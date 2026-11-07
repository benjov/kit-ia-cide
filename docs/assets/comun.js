// Kit IA-CIDE · barra de navegación, tema y utilidades compartidas
(function () {
  const raiz = document.documentElement;
  const base = raiz.dataset.base || ".";
  try { const t = localStorage.getItem("tema"); if (t) raiz.dataset.theme = t; } catch (e) {}

  const paginas = [
    ["index.html", "Inicio"],
    ["guia.html", "Guía de la sesión"],
    ["caso.html", "Caso completo"],
    ["herramientas/auditor.html", "Auditor de citas"],
    ["herramientas/kappa.html", "Simulador kappa"],
    ["herramientas/costos.html", "Costos"],
    ["kit.html", "Descargar kit"],
  ];
  const actual = location.pathname.split("/").slice(-2).join("/");
  const nav = paginas.map(([href, txt]) => {
    const activo = actual.endsWith(href) || (href === "index.html" && /\/(docs\/)?$/.test(location.pathname));
    return `<a href="${base}/${href}"${activo ? ' aria-current="page"' : ""}>${txt}</a>`;
  }).join("");
  const barra = document.createElement("header");
  barra.className = "barra";
  barra.innerHTML = `<div class="contenedor"><a class="marca" href="${base}/index.html"><span>CIDE</span> Kit IA · Sesión 4</a>
    <nav class="nav" aria-label="Principal">${nav}</nav>
    <button class="tema" type="button" aria-label="Cambiar tema claro/oscuro">◐</button></div>`;
  document.body.prepend(barra);
  barra.querySelector(".tema").addEventListener("click", () => {
    const oscuro = raiz.dataset.theme ? raiz.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    raiz.dataset.theme = oscuro ? "light" : "dark";
    try { localStorage.setItem("tema", raiz.dataset.theme); } catch (e) {}
  });

  const pie = document.createElement("footer");
  pie.innerHTML = `<div class="contenedor">Kit IA-CIDE · Sesión 4 "Del codebook al hallazgo" · Corpus: Sentencias emblemáticas, DGDH-SCJN (documentos públicos).
    Material docente; los resultados son ilustrativos y no constituyen análisis jurídico.</div>`;
  document.body.append(pie);
})();

// Utilidades
window.KIT = {
  async json(ruta) { const r = await fetch(ruta); if (!r.ok) throw new Error(ruta); return r.json(); },
  pct(x, d = 0) { return (x * 100).toFixed(d) + "%"; },
  esc(s) { return String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); },
  // Barras horizontales en SVG accesible
  barras(el, datos, { max = null, formato = v => v, color = "var(--acento)" } = {}) {
    const m = max ?? Math.max(...datos.map(d => d.valor), 1);
    el.innerHTML = datos.map(d => `
      <div style="display:grid;grid-template-columns:minmax(110px,38%) 1fr auto;gap:10px;align-items:center;margin:6px 0">
        <span style="font-size:.88rem;color:var(--texto-suave)">${KIT.esc(d.etiqueta)}</span>
        <span style="background:var(--superficie-2);border-radius:6px;height:18px;overflow:hidden">
          <span style="display:block;height:100%;width:${(d.valor / m) * 100}%;background:${d.color || color};border-radius:6px;transition:width .6s"></span></span>
        <span style="font-variant-numeric:tabular-nums;font-size:.88rem;min-width:3.5em;text-align:right">${formato(d.valor, d)}</span>
      </div>`).join("");
  },
};
