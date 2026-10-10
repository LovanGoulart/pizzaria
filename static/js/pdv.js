let categorias = [], produtos = [], carrinho = [], catAtual = "";
let produtoPendente = null;

async function carregar() {
  categorias = await (await fetch("/api/categorias")).json();
  produtos = await (await fetch("/api/produtos?so_ativos=1")).json();
  document.getElementById("listaCats").innerHTML = categorias.map(c =>
    '<button class="cat-btn" onclick="filtrarCat(\'' + c.id + '\', this)"><span>' + c.icone + '</span> ' + c.nome + '</button>'
  ).join("");
  renderProdutos();
}
function filtrarCat(id, btn) {
  catAtual = id;
  document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
  if (btn) btn.classList.add("active");
  renderProdutos();
}
function renderProdutos() {
  const busca = (document.getElementById("busca").value || "").toLowerCase();
  const grid = document.getElementById("produtosGrid");
  const lista = produtos.filter(p => {
    if (catAtual && String(p.categoria_id) !== String(catAtual)) return false;
    if (busca && !p.nome.toLowerCase().includes(busca)) return false;
    return true;
  });
  if (lista.length === 0) { grid.innerHTML = '<div class="vazio-box">Nenhum produto</div>'; return; }
  grid.innerHTML = lista.map(p =>
    '<div class="prod-card" onclick="addCarrinho(' + p.id + ')">' +
    '<div class="prod-cat">' + p.categoria_icone + " " + p.categoria_nome + '</div>' +
    '<div class="prod-nome">' + p.nome + '</div>' +
    (p.descricao ? '<div class="prod-desc">' + p.descricao + '</div>' : '') +
    '<div class="prod-preco">' + fmt(p.preco) + '</div></div>'
  ).join("");
}

// Ao clicar no produto: pergunta mesa e cliente antes de adicionar
function addCarrinho(id) {
  const p = produtos.find(x => x.id === id);
  if (!p) return;
  produtoPendente = p;
  document.getElementById("modalProdNome").textContent = p.nome;
  document.getElementById("mMesa").value = document.getElementById("mesa").value;
  document.getElementById("mCliente").value = document.getElementById("cliente").value;
  document.getElementById("modalProd").classList.remove("hidden");
  setTimeout(function() { document.getElementById("mMesa").focus(); }, 60);
}
function fecharModalProd() {
  produtoPendente = null;
  document.getElementById("modalProd").classList.add("hidden");
}
function confirmarProd() {
  if (!produtoPendente) return;
  const mesa = document.getElementById("mMesa").value.trim();
  if (!mesa) { toast("Informe a mesa", "erro"); return; }
  // Preenche automaticamente os campos do pedido
  document.getElementById("mesa").value = mesa;
  document.getElementById("cliente").value = document.getElementById("mCliente").value.trim();
  const id = produtoPendente.id;
  const nome = produtoPendente.nome;
  const preco = produtoPendente.preco;
  fecharModalProd();
  const ex = carrinho.find(x => x.produto_id === id);
  if (ex) ex.quantidade++;
  else carrinho.push({produto_id: id, nome: nome, preco: preco, quantidade: 1});
  renderCarrinho();
  toast(nome + " adicionado · Mesa " + mesa);
}

function altQtd(idx, delta) {
  carrinho[idx].quantidade += delta;
  if (carrinho[idx].quantidade <= 0) carrinho.splice(idx, 1);
  renderCarrinho();
}
function remover(idx) { carrinho.splice(idx, 1); renderCarrinho(); }
function renderCarrinho() {
  const el = document.getElementById("carrinhoItens");
  if (carrinho.length === 0) { el.innerHTML = '<div class="vazio">Nenhum item</div>'; atualizarTotal(); return; }
  el.innerHTML = carrinho.map((it, i) =>
    '<div class="item-carrinho"><div class="item-info"><div class="item-nome">' + it.nome + '</div><div class="item-preco">' + fmt(it.preco) + '</div></div><div class="item-qtd"><button class="menos" onclick="altQtd(' + i + ',-1)">−</button><span>' + it.quantidade + '</span><button onclick="altQtd(' + i + ',1)">+</button></div><div class="item-sub">' + fmt(it.preco * it.quantidade) + '</div><button class="btn small danger" onclick="remover(' + i + ')" style="padding:4px 8px">✕</button></div>'
  ).join("");
  atualizarTotal();
}
function atualizarTotal() {
  const sub = carrinho.reduce((s, it) => s + it.preco * it.quantidade, 0);
  const tax = +document.getElementById("taxaEntrega").value || 0;
  document.getElementById("subtotal").textContent = fmt(sub);
  document.getElementById("taxa").textContent = fmt(tax);
  document.getElementById("total").textContent = fmt(sub + tax);
}
function toggleEntrega() {
  const tipo = document.getElementById("tipoPedido").value;
  document.getElementById("endereco").style.display = tipo === "entrega" ? "block" : "none";
  document.getElementById("taxaEntrega").style.display = tipo === "entrega" ? "block" : "none";
  document.getElementById("mesa").style.display = tipo === "mesa" ? "block" : "none";
  if (tipo !== "entrega") document.getElementById("taxaEntrega").value = 0;
  atualizarTotal();
}
async function finalizar() {
  if (carrinho.length === 0) { toast("Carrinho vazio", "erro"); return; }
  const dados = {
    cliente: document.getElementById("cliente").value,
    tipo: document.getElementById("tipoPedido").value,
    mesa: document.getElementById("mesa").value,
    endereco: document.getElementById("endereco").value,
    taxa_entrega: +document.getElementById("taxaEntrega").value || 0,
    forma_pagamento: document.getElementById("formaPagamento").value,
    observacao: document.getElementById("obs").value,
    itens: carrinho.map(it => ({produto_id: it.produto_id, quantidade: it.quantidade}))
  };
  const r = await fetch("/api/pedidos", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(dados)});
  if (r.ok) { const p = await r.json(); toast("Pedido #" + p.numero + " criado!"); limpar(); }
  else toast("Erro ao criar pedido", "erro");
}
function limpar() {
  carrinho = [];
  ["cliente","mesa","endereco","obs","formaPagamento"].forEach(id => document.getElementById(id).value = "");
  document.getElementById("taxaEntrega").value = 0;
  renderCarrinho();
}
carregar();
toggleEntrega();
