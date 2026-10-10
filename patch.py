"""PATCH v5 - Restaurante Manager generico
Aplica mudancas pontuais nos arquivos existentes. Curto e seguro.
"""
from pathlib import Path

ROOT = Path('.')

# ============================================================
# 1) templates/base.html - branding generico + mobile limpo
# ============================================================
BASE_HTML = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}Restaurante Manager{% endblock %}</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
<header class="topbar">
  <div class="logo">🍽️ Restaurante Manager</div>
  <nav id="nav" class="topnav">
    {% if usuario_logado.role in ('admin', 'garcom') %}
      <a href="/" class="{% if request.path == '/' %}on{% endif %}">🧾 PDV</a>
    {% endif %}
    <a href="/pedidos" class="{% if request.path == '/pedidos' %}on{% endif %}">📋 Pedidos</a>
    {% if usuario_logado.role == 'admin' %}
      <a href="/produtos" class="{% if request.path == '/produtos' %}on{% endif %}">🍕 Produtos</a>
      <a href="/categorias" class="{% if request.path == '/categorias' %}on{% endif %}">📂 Categorias</a>
      <a href="/caixa" class="{% if request.path == '/caixa' %}on{% endif %}">💰 Caixa</a>
      <a href="/dashboard" class="{% if request.path == '/dashboard' %}on{% endif %}">📊 Dashboard</a>
      <a href="/usuarios" class="{% if request.path == '/usuarios' %}on{% endif %}">👥 Equipe</a>
    {% endif %}
  </nav>
  {% if usuario_logado %}
  <div class="user-box">
    <span class="user-nome">
      👤 {{ usuario_logado.nome }}
      <span class="role-badge role-{{ usuario_logado.role }}">{{ usuario_logado.role }}</span>
    </span>
    <a href="/logout" class="btn-sair" title="Sair">Sair</a>
  </div>
  {% endif %}
</header>
<main class="container">
  {% block content %}{% endblock %}
</main>

{% if usuario_logado %}
<!-- Menu rodape (SOMENTE mobile).
     Ordem: Pedidos, PDV, Caixa, Dashboard, Produtos, Categorias, Equipe -->
<nav class="bottom-nav">
  <a href="/pedidos" class="{% if request.path == '/pedidos' %}on{% endif %}">
    <span class="icon">📋</span><span>Pedidos</span>
  </a>
  {% if usuario_logado.role in ('admin', 'garcom') %}
  <a href="/" class="{% if request.path == '/' %}on{% endif %}">
    <span class="icon">🧾</span><span>PDV</span>
  </a>
  {% endif %}
  {% if usuario_logado.role == 'admin' %}
  <a href="/caixa" class="{% if request.path == '/caixa' %}on{% endif %}">
    <span class="icon">💰</span><span>Caixa</span>
  </a>
  <a href="/dashboard" class="{% if request.path == '/dashboard' %}on{% endif %}">
    <span class="icon">📊</span><span>Dash</span>
  </a>
  <a href="/produtos" class="{% if request.path == '/produtos' %}on{% endif %}">
    <span class="icon">🍕</span><span>Produtos</span>
  </a>
  <a href="/categorias" class="{% if request.path == '/categorias' %}on{% endif %}">
    <span class="icon">📂</span><span>Categ.</span>
  </a>
  <a href="/usuarios" class="{% if request.path == '/usuarios' %}on{% endif %}">
    <span class="icon">👥</span><span>Equipe</span>
  </a>
  {% endif %}
</nav>
{% endif %}

<div id="toast" class="toast"></div>
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
{% block scripts %}{% endblock %}
</body>
</html>
'''

# ============================================================
# 2) CSS adicional - SOBRESCREVE regras de topbar e bottom-nav
# ============================================================
CSS_PATCH = '''

/* ============================================================
   PATCH v5 - Menu superior apenas no desktop.
   No mobile o unico menu e o bottom-nav (rodape).
   ============================================================ */
.topnav { display: flex; }

@media (max-width: 900px) {
  .topnav { display: none !important; }
  .user-box { margin-left: auto; }
}

/* Bottom-nav: escondido no desktop, visivel no mobile */
.bottom-nav { display: none !important; }
@media (max-width: 900px) {
  .bottom-nav {
    display: flex !important;
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 60;
    background: linear-gradient(180deg, #8a2a1a, #5a1a0a);
    box-shadow: 0 -4px 20px rgba(0,0,0,.25);
    padding: 4px 2px calc(4px + env(safe-area-inset-bottom, 0px));
  }
  .bottom-nav a {
    flex: 1; display: flex; flex-direction: column; align-items: center;
    gap: 2px; padding: 8px 2px; color: #f0d8c8;
    font-size: 10px; font-weight: 600; border-radius: 10px;
    min-width: 0; white-space: nowrap;
  }
  .bottom-nav a .icon { font-size: 20px; line-height: 1; }
  .bottom-nav a.on { background: rgba(255,255,255,.18); color: #fff; }
  .container { padding-bottom: 96px; }
  .toast { bottom: 96px; }

  .topbar {
    padding: 10px 14px; height: auto; min-height: 54px; gap: 10px;
    flex-wrap: wrap; justify-content: space-between;
  }
  .logo { font-size: 15px; }
}

/* Destaque ainda maior da mesa */
.mesa-badge {
  display: block; text-align: center;
  background: linear-gradient(180deg, #c83828, #8a2a1a);
  color: #fff; font-size: 20px; font-weight: 900;
  letter-spacing: .8px; padding: 10px 18px; border-radius: 10px;
  margin: 10px 0; box-shadow: 0 4px 14px rgba(138,42,26,.35);
  text-transform: uppercase;
}
@media (max-width: 640px) {
  .mesa-badge { font-size: 24px; padding: 12px 20px; }
}
'''

# ============================================================
# 3) Aplicar alteracoes
# ============================================================
def aplicar():
    base = ROOT / 'templates' / 'base.html'
    base.parent.mkdir(parents=True, exist_ok=True)
    base.write_text(BASE_HTML, encoding='utf-8')
    print('  [OK] templates/base.html')

    css = ROOT / 'static' / 'css' / 'style.css'
    if css.exists():
        txt = css.read_text(encoding='utf-8')
        # remove patch anterior se existir
        marker = '/* ============================================================\n   PATCH v5'
        if marker in txt:
            txt = txt.split(marker)[0]
        css.write_text(txt + CSS_PATCH, encoding='utf-8')
        print('  [OK] static/css/style.css (patch aplicado no final)')
    else:
        print('  [AVISO] style.css nao encontrado - crie a pasta static/css/')

    # login / registro - branding generico
    for name in ('login.html', 'registro.html'):
        p = ROOT / 'templates' / name
        if p.exists():
            t = p.read_text(encoding='utf-8')
            t = t.replace('Pizzaria Manager', 'Restaurante Manager')
            t = t.replace('sua pizzaria', 'seu restaurante')
            t = t.replace('🍕', '🍽️', 1)  # apenas o logo do topo
            t = t.replace('admin@pizzaria.com', 'admin@restaurante.com')
            p.write_text(t, encoding='utf-8')
            print('  [OK] templates/' + name)

    # config.py - nome do banco
    cfg = ROOT / 'config.py'
    if cfg.exists():
        t = cfg.read_text(encoding='utf-8')
        t = t.replace('sqlite:///pizzaria.db', 'sqlite:///restaurante.db')
        cfg.write_text(t, encoding='utf-8')
        print('  [OK] config.py')

    # init_db.py - emails genericos
    ini = ROOT / 'init_db.py'
    if ini.exists():
        t = ini.read_text(encoding='utf-8')
        t = t.replace('@pizzaria.com', '@restaurante.com')
        t = t.replace('Pizzaria Manager', 'Restaurante Manager')
        ini.write_text(t, encoding='utf-8')
        print('  [OK] init_db.py')

    print()
    print('PATCH APLICADO COM SUCESSO!')
    print()
    print('Agora rode:')
    print('  python init_db.py')
    print('  python app.py')

if __name__ == '__main__':
    aplicar()