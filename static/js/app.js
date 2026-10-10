function toast(msg, tipo) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = "toast show" + (tipo === "erro" ? " erro" : "");
  setTimeout(function() { el.className = "toast"; }, 2200);
}
function toggleMenu() {
  document.getElementById("nav").classList.toggle("open");
}
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") {
    const m = document.getElementById("modal");
    if (m) m.classList.add("hidden");
  }
});
document.addEventListener("click", function(e) {
  if (e.target.id === "modal") e.target.classList.add("hidden");
});
function fmt(v) { return "R$ " + v.toFixed(2).replace(".", ","); }
