"""
StreamView Analytics - EA2
Treemap de géneros en D3.js (v7). Python prepara los datos (JSON) y D3 dibuja.

Se usa de dos formas:
  - incrustado en el dashboard analítico de Streamlit (components.html)
  - como archivo autónomo: python src/export/build_d3.py -> d3/treemap_generos.html
"""

import json

PLANTILLA = r"""
<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<style>
  body { margin:0; font-family: "Segoe UI", system-ui, sans-serif; color:#1f2937; }
  #barra { display:flex; align-items:center; gap:10px; padding:4px 2px 8px; font-size:13px; }
  select { padding:3px 6px; border:1px solid #cbd5e1; border-radius:6px; font-size:13px; }
  #tip { position:absolute; pointer-events:none; background:#111827; color:#fff; padding:6px 9px;
         border-radius:6px; font-size:12px; line-height:1.4; opacity:0; transition:opacity .1s; }
  #leyenda { margin-left:auto; display:flex; align-items:center; gap:6px; font-size:12px; }
  #grad { width:120px; height:10px; border-radius:3px; }
  svg text { pointer-events:none; }
</style></head>
<body>
<div id="barra">
  <b>__TITULO__</b>
  <span>Color:</span>
  <select id="metrica">
    <option value="calificacion">Calificación promedio</option>
    <option value="popularidad">Popularidad promedio</option>
  </select>
  <div id="leyenda"><span id="lmin"></span><div id="grad"></div><span id="lmax"></span></div>
</div>
<div id="tip"></div>
<svg id="lienzo" width="100%" height="__ALTO__" viewBox="0 0 __ANCHO__ __ALTO__" preserveAspectRatio="xMidYMid meet"></svg>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<script>
const datos = __DATOS__;
const W = __ANCHO__, H = __ALTO__;
const fmt = d3.format(",.0f");
const svg = d3.select("#lienzo");
const tip = d3.select("#tip");

const raiz = d3.hierarchy({ children: datos }).sum(d => d.titulos).sort((a, b) => b.value - a.value);
d3.treemap().size([W, H]).paddingInner(2).round(true)(raiz);

const nodos = svg.selectAll("g").data(raiz.leaves()).join("g")
  .attr("transform", d => `translate(${d.x0},${d.y0})`);
const rects = nodos.append("rect")
  .attr("width", d => d.x1 - d.x0).attr("height", d => d.y1 - d.y0).attr("rx", 3);
nodos.append("text").attr("x", 6).attr("y", 16).attr("font-size", 12).attr("font-weight", 600)
  .text(d => (d.x1 - d.x0 > 70 && d.y1 - d.y0 > 24) ? d.data.genero : "");
nodos.append("text").attr("x", 6).attr("y", 31).attr("font-size", 11)
  .text(d => (d.x1 - d.x0 > 70 && d.y1 - d.y0 > 40) ? fmt(d.data.titulos) + " títulos" : "");

nodos.on("mousemove", (ev, d) => {
  tip.style("opacity", 1).style("left", (ev.pageX + 12) + "px").style("top", (ev.pageY + 12) + "px")
     .html(`<b>${d.data.genero}</b><br>${fmt(d.data.titulos)} títulos<br>` +
           `Calificación prom.: ${d.data.calificacion.toFixed(2)}<br>Popularidad prom.: ${d.data.popularidad.toFixed(1)}`);
}).on("mouseleave", () => tip.style("opacity", 0));

function pintar(metrica) {
  const vals = datos.map(d => d[metrica]);
  const esc = d3.scaleSequential(d3.interpolateBlues).domain([d3.min(vals) * 0.9, d3.max(vals)]);
  rects.transition().duration(300).attr("fill", d => esc(d.data[metrica]));
  nodos.selectAll("text").attr("fill", d => esc(d.data[metrica]) && d3.hsl(esc(d.data[metrica])).l < 0.55 ? "#fff" : "#111827");
  const r = metrica === "calificacion" ? 2 : 1;
  d3.select("#lmin").text(d3.min(vals).toFixed(r));
  d3.select("#lmax").text(d3.max(vals).toFixed(r));
  d3.select("#grad").style("background", `linear-gradient(to right, ${esc(d3.min(vals))}, ${esc(d3.max(vals))})`);
}
d3.select("#metrica").on("change", e => pintar(e.target.value));
pintar("calificacion");
</script></body></html>
"""


def construir_html_treemap(tabla_generos, titulo="Géneros por volumen (tamaño = títulos)", ancho=900, alto=420):
    """tabla_generos: DataFrame con columnas genero, titulos, calificacion, popularidad."""
    filas = [
        {
            "genero": str(r.genero),
            "titulos": int(r.titulos),
            "calificacion": float(r.calificacion) if r.calificacion == r.calificacion else 0.0,
            "popularidad": float(r.popularidad),
        }
        for r in tabla_generos.itertuples()
    ]
    return (
        PLANTILLA.replace("__DATOS__", json.dumps(filas, ensure_ascii=False))
        .replace("__TITULO__", titulo)
        .replace("__ANCHO__", str(ancho))
        .replace("__ALTO__", str(alto))
    )
