from datetime import datetime, date
from functools import wraps
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from config import Config
from models import db, Usuario, Categoria, Produto, Pedido, ItemPedido, Caixa, Movimento

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

ROTAS_PUBLICAS = {"login", "registro", "static"}

# Paginas e os papeis que podem acessa-las
PERMISSOES_PAGINAS = {
    "pdv": ("admin", "garcom"),
    "pedidos": ("admin", "garcom", "cozinha"),
    "produtos": ("admin",),
    "categorias": ("admin",),
    "caixa": ("admin",),
    "dashboard": ("admin",),
    "usuarios": ("admin",),
}


def requer_role(*roles):
    def deco(fn):
        @wraps(fn)
        def wrapper(*a, **kw):
            if session.get("role") not in roles:
                if request.path.startswith("/api/"):
                    return jsonify({"erro": "Sem permissao"}), 403
                return redirect(url_for("pedidos"))
            return fn(*a, **kw)
        return wrapper
    return deco


def tenant():
    return session.get("admin_id") or session.get("user_id")


@app.before_request
def controlar_acesso():
    ep = request.endpoint
    if ep in ROTAS_PUBLICAS or ep is None or ep == "static":
        return
    if "user_id" not in session:
        if request.path.startswith("/api/"):
            return jsonify({"erro": "Nao autorizado"}), 401
        return redirect(url_for("login"))
    roles_permitidos = PERMISSOES_PAGINAS.get(ep)
    if roles_permitidos and session.get("role") not in roles_permitidos:
        if request.path.startswith("/api/"):
            return jsonify({"erro": "Sem permissao"}), 403
        if session.get("role") == "cozinha":
            return redirect(url_for("pedidos"))
        return redirect(url_for("pdv"))


@app.context_processor
def injetar_usuario():
    u = None
    if "user_id" in session:
        u = Usuario.query.get(session["user_id"])
    return {"usuario_logado": u}


# ============================================================
# AUTENTICACAO
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        u = Usuario.query.filter_by(email=email).first()
        if u and check_password_hash(u.senha_hash, senha):
            session["user_id"] = u.id
            session["role"] = u.role
            session["admin_id"] = u.admin_id if u.admin_id else u.id
            # Tela inicial: garcom vai pro PDV; admin e cozinha vao pra Pedidos
            if u.role == "garcom":
                return redirect(url_for("pdv"))
            return redirect(url_for("pedidos"))
        return render_template("login.html", erro="E-mail ou senha invalidos")
    return render_template("login.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        if not nome or not email or not senha:
            return render_template("registro.html", erro="Preencha todos os campos")
        if len(senha) < 4:
            return render_template("registro.html", erro="Senha deve ter ao menos 4 caracteres")
        if Usuario.query.filter_by(email=email).first():
            return render_template("registro.html", erro="E-mail ja cadastrado")
        u = Usuario(nome=nome, email=email,
                    senha_hash=generate_password_hash(senha),
                    role="admin", admin_id=None)
        db.session.add(u); db.session.commit()
        seed_cardapio_padrao(u.id)
        session["user_id"] = u.id
        session["role"] = "admin"
        session["admin_id"] = u.id
        return redirect(url_for("pedidos"))
    return render_template("registro.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================================
# PAGINAS
# ============================================================
@app.route("/")
def pdv(): return render_template("pdv.html")

@app.route("/pedidos")
def pedidos(): return render_template("pedidos.html")

@app.route("/produtos")
def produtos(): return render_template("produtos.html")

@app.route("/categorias")
def categorias(): return render_template("categorias.html")

@app.route("/caixa")
def caixa(): return render_template("caixa.html")

@app.route("/dashboard")
def dashboard(): return render_template("dashboard.html")

@app.route("/usuarios")
def usuarios(): return render_template("usuarios.html")


# ============================================================
# API EQUIPE (somente admin)
# ============================================================
@app.route("/api/usuarios", methods=["GET"])
@requer_role("admin")
def api_listar_usuarios():
    us = Usuario.query.filter_by(admin_id=tenant()).all()
    return jsonify([u.to_dict() for u in us])


@app.route("/api/usuarios", methods=["POST"])
@requer_role("admin")
def api_criar_usuario():
    d = request.json
    if d.get("role") not in ("garcom", "cozinha"):
        return jsonify({"erro": "Funcao invalida. Use garcom ou cozinha"}), 400
    email = d["email"].strip().lower()
    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "E-mail ja cadastrado"}), 400
    if len(d.get("senha", "")) < 4:
        return jsonify({"erro": "Senha deve ter ao menos 4 caracteres"}), 400
    u = Usuario(nome=d["nome"], email=email,
                senha_hash=generate_password_hash(d["senha"]),
                role=d["role"], admin_id=tenant())
    db.session.add(u); db.session.commit()
    return jsonify(u.to_dict()), 201


@app.route("/api/usuarios/<int:uid>", methods=["PUT"])
@requer_role("admin")
def api_editar_usuario(uid):
    u = Usuario.query.filter_by(id=uid, admin_id=tenant()).first_or_404()
    d = request.json
    if "nome" in d: u.nome = d["nome"]
    if "email" in d:
        email = d["email"].strip().lower()
        outro = Usuario.query.filter(Usuario.email == email, Usuario.id != uid).first()
        if outro: return jsonify({"erro": "E-mail ja em uso"}), 400
        u.email = email
    if d.get("role") in ("garcom", "cozinha"):
        u.role = d["role"]
    if d.get("nova_senha"):
        if len(d["nova_senha"]) < 4:
            return jsonify({"erro": "Senha deve ter ao menos 4 caracteres"}), 400
        u.senha_hash = generate_password_hash(d["nova_senha"])
    db.session.commit()
    return jsonify(u.to_dict())


@app.route("/api/usuarios/<int:uid>", methods=["DELETE"])
@requer_role("admin")
def api_deletar_usuario(uid):
    u = Usuario.query.filter_by(id=uid, admin_id=tenant()).first_or_404()
    db.session.delete(u); db.session.commit()
    return jsonify({"ok": True})


# ============================================================
# API CATEGORIAS
# ============================================================
@app.route("/api/categorias", methods=["GET"])
def api_categorias():
    cats = Categoria.query.filter_by(usuario_id=tenant()).order_by(Categoria.ordem, Categoria.nome).all()
    return jsonify([c.to_dict() for c in cats])


@app.route("/api/categorias", methods=["POST"])
@requer_role("admin")
def api_criar_categoria():
    d = request.json
    c = Categoria(usuario_id=tenant(), nome=d["nome"],
                  icone=d.get("icone", "🍕"), ordem=int(d.get("ordem", 0)))
    db.session.add(c); db.session.commit()
    return jsonify(c.to_dict()), 201


@app.route("/api/categorias/<int:cid>", methods=["PUT"])
@requer_role("admin")
def api_atualizar_categoria(cid):
    c = Categoria.query.filter_by(id=cid, usuario_id=tenant()).first_or_404()
    d = request.json
    for k in ("nome", "icone", "ordem"):
        if k in d: setattr(c, k, d[k])
    db.session.commit()
    return jsonify(c.to_dict())


@app.route("/api/categorias/<int:cid>", methods=["DELETE"])
@requer_role("admin")
def api_deletar_categoria(cid):
    c = Categoria.query.filter_by(id=cid, usuario_id=tenant()).first_or_404()
    db.session.delete(c); db.session.commit()
    return jsonify({"ok": True})


# ============================================================
# API PRODUTOS
# ============================================================
@app.route("/api/produtos", methods=["GET"])
def api_produtos():
    q = Produto.query.filter_by(usuario_id=tenant())
    if request.args.get("so_ativos") == "1":
        q = q.filter_by(ativo=True)
    cat = request.args.get("categoria_id")
    if cat:
        q = q.filter_by(categoria_id=int(cat))
    return jsonify([p.to_dict() for p in q.order_by(Produto.nome).all()])


@app.route("/api/produtos", methods=["POST"])
@requer_role("admin")
def api_criar_produto():
    d = request.json
    p = Produto(usuario_id=tenant(), nome=d["nome"],
                descricao=d.get("descricao"), preco=float(d.get("preco", 0)),
                categoria_id=int(d["categoria_id"]), ativo=bool(d.get("ativo", True)))
    db.session.add(p); db.session.commit()
    return jsonify(p.to_dict()), 201


@app.route("/api/produtos/<int:pid>", methods=["PUT"])
@requer_role("admin")
def api_atualizar_produto(pid):
    p = Produto.query.filter_by(id=pid, usuario_id=tenant()).first_or_404()
    d = request.json
    for k in ("nome", "descricao"):
        if k in d: setattr(p, k, d[k])
    if "preco" in d: p.preco = float(d["preco"])
    if "categoria_id" in d: p.categoria_id = int(d["categoria_id"])
    if "ativo" in d: p.ativo = bool(d["ativo"])
    db.session.commit()
    return jsonify(p.to_dict())


@app.route("/api/produtos/<int:pid>", methods=["DELETE"])
@requer_role("admin")
def api_deletar_produto(pid):
    p = Produto.query.filter_by(id=pid, usuario_id=tenant()).first_or_404()
    db.session.delete(p); db.session.commit()
    return jsonify({"ok": True})


# ============================================================
# API PEDIDOS
# ============================================================
@app.route("/api/pedidos", methods=["GET"])
def api_pedidos():
    q = Pedido.query.filter_by(usuario_id=tenant())
    if request.args.get("status"):
        if request.args["status"] == "nao_pagos":
            q = q.filter_by(pago=False)
        else:
            q = q.filter_by(status=request.args["status"])
    if request.args.get("hoje") == "1":
        q = q.filter(func.date(Pedido.criado_em) == date.today())
    return jsonify([p.to_dict() for p in q.order_by(Pedido.criado_em.desc()).all()])


@app.route("/api/pedidos/<int:pid>", methods=["GET"])
def api_pedido(pid):
    p = Pedido.query.filter_by(id=pid, usuario_id=tenant()).first_or_404()
    return jsonify(p.to_dict())


@app.route("/api/pedidos", methods=["POST"])
@requer_role("admin", "garcom")
def api_criar_pedido():
    d = request.json
    itens = d.get("itens", [])
    if not itens:
        return jsonify({"erro": "Pedido sem itens"}), 400
    tid = tenant()
    ultimo = db.session.query(func.max(Pedido.numero)).filter(Pedido.usuario_id == tid).scalar() or 0
    p = Pedido(usuario_id=tid, numero=ultimo + 1,
               cliente=d.get("cliente"), tipo=d.get("tipo", "mesa"),
               mesa=d.get("mesa"), endereco=d.get("endereco"),
               taxa_entrega=float(d.get("taxa_entrega", 0)),
               forma_pagamento=d.get("forma_pagamento"),
               observacao=d.get("observacao"), status="aberto", pago=False)
    db.session.add(p); db.session.flush()
    subtotal = 0.0
    for it in itens:
        prod = Produto.query.filter_by(id=it["produto_id"], usuario_id=tid).first()
        if not prod: continue
        qtd = int(it.get("quantidade", 1))
        sub = prod.preco * qtd
        db.session.add(ItemPedido(pedido_id=p.id, produto_id=prod.id,
            quantidade=qtd, preco_unit=prod.preco, subtotal=sub,
            observacao=it.get("observacao")))
        subtotal += sub
    p.subtotal = subtotal
    p.total = subtotal + p.taxa_entrega
    db.session.commit()
    return jsonify(p.to_dict()), 201


@app.route("/api/pedidos/<int:pid>/status", methods=["POST"])
def api_atualizar_status(pid):
    p = Pedido.query.filter_by(id=pid, usuario_id=tenant()).first_or_404()
    novo = request.json.get("status")
    role = session.get("role")

    if novo in ("em_preparo", "pronto"):
        if role not in ("admin", "cozinha"):
            return jsonify({"erro": "Somente cozinha pode fazer isso"}), 403
    elif novo == "entregue":
        if role not in ("admin", "garcom"):
            return jsonify({"erro": "Somente garcom pode fazer isso"}), 403
    elif novo == "cancelado":
        if role != "admin":
            return jsonify({"erro": "Somente admin pode cancelar"}), 403
    elif novo not in ("aberto",):
        return jsonify({"erro": "Status invalido"}), 400

    p.status = novo
    db.session.commit()
    return jsonify(p.to_dict())


@app.route("/api/pedidos/<int:pid>/pagar", methods=["POST"])
@requer_role("admin")
def api_pagar_pedido(pid):
    p = Pedido.query.filter_by(id=pid, usuario_id=tenant()).first_or_404()
    if p.pago:
        return jsonify({"erro": "Este pedido ja esta pago"}), 400
    if p.status == "cancelado":
        return jsonify({"erro": "Pedido cancelado nao pode ser pago"}), 400
    cx = Caixa.query.filter_by(status="aberto", usuario_id=tenant()).first()
    if not cx:
        return jsonify({"erro": "Abra o caixa antes de registrar pagamentos"}), 400
    forma = request.json.get("forma_pagamento") or p.forma_pagamento
    p.pago = True
    p.forma_pagamento = forma
    db.session.add(Movimento(caixa_id=cx.id, tipo="entrada",
        valor=p.total, descricao="Pagamento Pedido #" + str(p.numero),
        forma_pagamento=forma, pedido_id=p.id))
    db.session.commit()
    return jsonify(p.to_dict())


@app.route("/api/pedidos/<int:pid>", methods=["DELETE"])
@requer_role("admin")
def api_deletar_pedido(pid):
    p = Pedido.query.filter_by(id=pid, usuario_id=tenant()).first_or_404()
    db.session.delete(p); db.session.commit()
    return jsonify({"ok": True})


# ============================================================
# API CAIXA (somente admin)
# ============================================================
@app.route("/api/caixa/atual", methods=["GET"])
@requer_role("admin")
def api_caixa_atual():
    cx = Caixa.query.filter_by(status="aberto", usuario_id=tenant()).first()
    if not cx:
        return jsonify({"aberto": False})
    entradas = sum(m.valor for m in cx.movimentos if m.tipo == "entrada")
    saidas = sum(m.valor for m in cx.movimentos if m.tipo == "saida")
    return jsonify({"aberto": True, "caixa": cx.to_dict(),
                    "entradas": entradas, "saidas": saidas,
                    "saldo": cx.valor_inicial + entradas - saidas,
                    "movimentos": [m.to_dict() for m in cx.movimentos[::-1]]})


@app.route("/api/caixa/abrir", methods=["POST"])
@requer_role("admin")
def api_abrir_caixa():
    if Caixa.query.filter_by(status="aberto", usuario_id=tenant()).first():
        return jsonify({"erro": "Ja existe caixa aberto"}), 400
    cx = Caixa(usuario_id=tenant(), valor_inicial=float(request.json.get("valor_inicial", 0)))
    db.session.add(cx); db.session.commit()
    return jsonify(cx.to_dict()), 201


@app.route("/api/caixa/fechar", methods=["POST"])
@requer_role("admin")
def api_fechar_caixa():
    cx = Caixa.query.filter_by(status="aberto", usuario_id=tenant()).first()
    if not cx:
        return jsonify({"erro": "Nenhum caixa aberto"}), 400
    entradas = sum(m.valor for m in cx.movimentos if m.tipo == "entrada")
    saidas = sum(m.valor for m in cx.movimentos if m.tipo == "saida")
    cx.valor_final = cx.valor_inicial + entradas - saidas
    cx.status = "fechado"
    cx.fechamento = datetime.now()
    cx.observacao = request.json.get("observacao")
    db.session.commit()
    return jsonify(cx.to_dict())


@app.route("/api/caixa/movimento", methods=["POST"])
@requer_role("admin")
def api_movimento():
    cx = Caixa.query.filter_by(status="aberto", usuario_id=tenant()).first()
    if not cx:
        return jsonify({"erro": "Nenhum caixa aberto"}), 400
    d = request.json
    m = Movimento(caixa_id=cx.id, tipo=d.get("tipo", "entrada"),
                  valor=float(d.get("valor", 0)), descricao=d.get("descricao"),
                  forma_pagamento=d.get("forma_pagamento"))
    db.session.add(m); db.session.commit()
    return jsonify(m.to_dict()), 201


@app.route("/api/caixa/historico", methods=["GET"])
@requer_role("admin")
def api_historico_caixa():
    cx = Caixa.query.filter_by(usuario_id=tenant()).order_by(Caixa.abertura.desc()).limit(30).all()
    return jsonify([c.to_dict() for c in cx])


# ============================================================
# API DASHBOARD (somente admin)
# ============================================================
@app.route("/api/dashboard", methods=["GET"])
@requer_role("admin")
def api_dashboard():
    tid = tenant()
    hoje = date.today()
    pedidos_hoje = Pedido.query.filter(Pedido.usuario_id == tid,
                                       func.date(Pedido.criado_em) == hoje).all()
    entregues = [p for p in pedidos_hoje if p.status == "entregue"]
    abertos = [p for p in pedidos_hoje if p.status in ("aberto", "em_preparo", "pronto")]
    faturamento = sum(p.total for p in entregues)
    ticket = faturamento / len(entregues) if entregues else 0
    contagem = {}
    for p in entregues:
        for it in p.itens:
            nome = it.produto.nome if it.produto else "?"
            contagem[nome] = contagem.get(nome, 0) + it.quantidade
    top = sorted(contagem.items(), key=lambda x: -x[1])[:8]
    return jsonify({"faturamento": round(faturamento, 2),
                    "pedidos_entregues": len(entregues),
                    "pedidos_abertos": len(abertos),
                    "total_pedidos": len(pedidos_hoje),
                    "ticket_medio": round(ticket, 2),
                    "top_produtos": [{"nome": n, "qtd": q} for n, q in top]})


# ============================================================
# SEED CARDAPIO PADRAO
# ============================================================
def seed_cardapio_padrao(uid):
    cats = [("Pizzas Salgadas", "🍕", 1), ("Pizzas Doces", "🍫", 2),
            ("Bebidas", "🥤", 3), ("Porções", "🍟", 4), ("Sobremesas", "🍰", 5)]
    ids = {}
    for nome, icone, ordem in cats:
        c = Categoria(usuario_id=uid, nome=nome, icone=icone, ordem=ordem)
        db.session.add(c); db.session.flush()
        ids[nome] = c.id
    prod = [
        ("Calabresa", "Calabresa fatiada, cebola e mussarela", 45, "Pizzas Salgadas"),
        ("Margherita", "Mussarela, tomate e manjericão", 42, "Pizzas Salgadas"),
        ("Portuguesa", "Presunto, ovo, cebola, ervilha e mussarela", 48, "Pizzas Salgadas"),
        ("Quatro Queijos", "Mussarela, provolone, gorgonzola e parmesão", 52, "Pizzas Salgadas"),
        ("Frango com Catupiry", "Frango desfiado e catupiry", 49, "Pizzas Salgadas"),
        ("Pepperoni", "Pepperoni fatiado e mussarela", 50, "Pizzas Salgadas"),
        ("Bacon", "Bacon crocante e mussarela", 50, "Pizzas Salgadas"),
        ("Vegetariana", "Abobrinha, berinjela, tomate e mussarela", 46, "Pizzas Salgadas"),
        ("Chocolate", "Chocolate ao leite derretido", 42, "Pizzas Doces"),
        ("Chocolate com Morango", "Chocolate e morangos frescos", 48, "Pizzas Doces"),
        ("Prestígio", "Chocolate e coco", 46, "Pizzas Doces"),
        ("Coca-Cola 2L", "Refrigerante gelado", 14, "Bebidas"),
        ("Guaraná 2L", "Refrigerante gelado", 12, "Bebidas"),
        ("Cerveja Long Neck", "Heineken 330ml", 10, "Bebidas"),
        ("Água Mineral 500ml", "Sem gás", 5, "Bebidas"),
        ("Suco de Laranja 500ml", "Natural", 12, "Bebidas"),
        ("Batata Frita", "Porção individual com sal", 25, "Porções"),
        ("Batata com Cheddar e Bacon", "Porção generosa", 38, "Porções"),
        ("Frango a Passarinho", "Com alho e limão", 42, "Porções"),
        ("Petit Gateau", "Com sorvete de creme", 22, "Sobremesas"),
        ("Pudim", "Pudim de leite condensado", 15, "Sobremesas"),
    ]
    for nome, desc, preco, cn in prod:
        db.session.add(Produto(usuario_id=uid, nome=nome, descricao=desc,
                               preco=preco, categoria_id=ids[cn]))
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
