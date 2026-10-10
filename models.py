from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="admin")  # admin | garcom | cozinha
    admin_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email,
                "role": self.role,
                "criado_em": self.criado_em.strftime("%d/%m/%Y")}


class Categoria(db.Model):
    __tablename__ = "categorias"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    icone = db.Column(db.String(10), default="🍕")
    ordem = db.Column(db.Integer, default=0)
    produtos = db.relationship("Produto", backref="categoria", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "icone": self.icone,
                "ordem": self.ordem, "total_produtos": len(self.produtos)}


class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(255))
    preco = db.Column(db.Float, nullable=False, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao,
                "preco": self.preco, "categoria_id": self.categoria_id,
                "categoria_nome": self.categoria.nome if self.categoria else None,
                "categoria_icone": self.categoria.icone if self.categoria else "🍕",
                "ativo": self.ativo}


class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    cliente = db.Column(db.String(120))
    tipo = db.Column(db.String(20), default="mesa")
    mesa = db.Column(db.String(10))
    endereco = db.Column(db.String(255))
    status = db.Column(db.String(20), default="aberto")
    pago = db.Column(db.Boolean, default=False)
    subtotal = db.Column(db.Float, default=0)
    taxa_entrega = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    forma_pagamento = db.Column(db.String(20))
    observacao = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    itens = db.relationship("ItemPedido", backref="pedido", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "numero": self.numero, "cliente": self.cliente,
                "tipo": self.tipo, "mesa": self.mesa, "endereco": self.endereco,
                "status": self.status, "pago": self.pago,
                "subtotal": self.subtotal,
                "taxa_entrega": self.taxa_entrega, "total": self.total,
                "forma_pagamento": self.forma_pagamento, "observacao": self.observacao,
                "criado_em": self.criado_em.strftime("%d/%m/%Y %H:%M"),
                "atualizado_em": self.atualizado_em.strftime("%d/%m/%Y %H:%M"),
                "itens": [i.to_dict() for i in self.itens],
                "qtd_itens": sum(i.quantidade for i in self.itens)}


class ItemPedido(db.Model):
    __tablename__ = "itens_pedido"
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    preco_unit = db.Column(db.Float, default=0)
    subtotal = db.Column(db.Float, default=0)
    observacao = db.Column(db.String(255))
    produto = db.relationship("Produto")

    def to_dict(self):
        return {"id": self.id, "produto_id": self.produto_id,
                "produto_nome": self.produto.nome if self.produto else "?",
                "quantidade": self.quantidade, "preco_unit": self.preco_unit,
                "subtotal": self.subtotal, "observacao": self.observacao}


class Caixa(db.Model):
    __tablename__ = "caixas"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    valor_inicial = db.Column(db.Float, default=0)
    valor_final = db.Column(db.Float)
    status = db.Column(db.String(20), default="aberto")
    abertura = db.Column(db.DateTime, default=datetime.now)
    fechamento = db.Column(db.DateTime)
    observacao = db.Column(db.Text)
    movimentos = db.relationship("Movimento", backref="caixa", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "valor_inicial": self.valor_inicial,
                "valor_final": self.valor_final, "status": self.status,
                "abertura": self.abertura.strftime("%d/%m/%Y %H:%M"),
                "fechamento": self.fechamento.strftime("%d/%m/%Y %H:%M") if self.fechamento else None,
                "observacao": self.observacao}


class Movimento(db.Model):
    __tablename__ = "movimentos"
    id = db.Column(db.Integer, primary_key=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey("caixas.id"), nullable=False)
    tipo = db.Column(db.String(20), default="entrada")
    valor = db.Column(db.Float, default=0)
    descricao = db.Column(db.String(255))
    forma_pagamento = db.Column(db.String(20))
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"))
    criado_em = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {"id": self.id, "tipo": self.tipo, "valor": self.valor,
                "descricao": self.descricao, "forma_pagamento": self.forma_pagamento,
                "pedido_id": self.pedido_id,
                "criado_em": self.criado_em.strftime("%d/%m/%Y %H:%M")}
