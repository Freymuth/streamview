"""
StreamView Analytics - EA3
Página 3 · CALIDAD DE DATOS Y EDA (Equipo de Data & Analytics, y respaldo para todas las áreas).

Sigue la estrategia analítica de la guía 3.1.1 (Visual Analytics y EDA):
  Paso 4  Evaluar la calidad de los datos      -> pestaña «Calidad»
  Paso 5  Analizar cada variable               -> pestaña «Distribuciones»
  Paso 6  Explorar relaciones entre variables  -> pestaña «Relaciones»
  Paso 7  Identificar patrones / anomalías     -> pestaña «Anomalías»
Responde la limitación detectada en la evaluación crítica: el dashboard mostraba
resultados, pero no dejaba ver qué tan confiables eran los datos detrás.
"""

import sys

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(".")
from dashboard import utils as u  # noqa: E402

st.set_page_config(page_title="Calidad y EDA · StreamView", page_icon="🧪", layout="wide")

catalogo, financiero = u.cargar_datos()
f = u.sidebar_filtros(catalogo, analitico=False)
df = u.aplicar_filtros(catalogo, f)

st.title("🧪 Calidad de datos y análisis exploratorio")
st.caption("Equipo de Data & Analytics · " + u.alcance(f, len(df)))
if df.empty:
    st.warning("No hay títulos con los filtros actuales.")
    st.stop()

tabs = st.tabs(["✅ Calidad (paso 4)", "📊 Distribuciones (paso 5)", "🔗 Relaciones (paso 6)", "⚠️ Anomalías (paso 7)"])

# --------------------------------------------------------------- Calidad ----
with tabs[0]:
    st.subheader("¿Qué tan completos y confiables son los datos?")
    cols = {"calificacion": "Calificación (≥ 10 votos)", "budget": "Presupuesto", "revenue": "Ingresos",
            "director": "Director", "country": "País", "genres": "Género", "description": "Descripción"}
    filas = []
    for c, nombre in cols.items():
        serie = df[c]
        faltan = serie.isna().sum() + (serie == "Desconocido").sum()
        filas.append({"Campo": nombre, "Faltantes": int(faltan), "% faltante": faltan / len(df) * 100})
    q = pd.DataFrame(filas).sort_values("% faltante", ascending=False)
    fig = px.bar(q, x="% faltante", y="Campo", orientation="h", text=q["% faltante"].map(lambda v: f"{u.d(v, 1)}%"),
                 color_discrete_sequence=[u.NARANJA])
    fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(u.estilo(fig, "Porcentaje de datos faltantes por campo", 360), width="stretch")
    c1, c2, c3 = st.columns(3)
    c1.metric("Títulos con calificación válida", f"{u.d(df['calificacion'].notna().mean() * 100, 1)}%",
              help="Solo cuenta con ≥ 10 votos. Con menos, la nota es ruido.")
    c2.metric("Películas con datos financieros",
              f"{u.d(df[(df['type'] == 'Movie') & df['uid'].isin(financiero['uid'])].shape[0] / max((df['type'] == 'Movie').sum(), 1) * 100, 1)}%",
              help="Presupuesto e ingresos informados (0 se trató como dato no disponible).")
    c3.metric("Presupuestos no realistas excluidos", u.n((~financiero["presupuesto_realista"]).sum()),
              help="Películas con presupuesto < USD 10.000: producen ROI de millones de veces.")
    st.info("Regla aplicada: un 0 en presupuesto, ingresos o votos significa **«dato no disponible»**, no «cero». "
            "Por eso se excluye de los promedios en lugar de arrastrarlos hacia abajo.")
    st.caption("Detalle de cada decisión de limpieza: `reports/data_quality/cleaning_summary.csv`.")

# --------------------------------------------------------- Distribuciones ----
with tabs[1]:
    st.subheader("¿Cómo se distribuye cada variable?")
    var = st.radio("Variable", ["Calificación", "Popularidad", "Votos", "Año de estreno"], horizontal=True)
    mapa = {"Calificación": "calificacion", "Popularidad": "popularity", "Votos": "vote_count", "Año de estreno": "release_year"}
    col = mapa[var]
    datos = df.dropna(subset=[col])
    logx = var in ("Popularidad", "Votos")
    if logx:
        datos = datos[datos[col] > 0]
    a, b = st.columns(2)
    with a:
        fig = px.histogram(datos, x=col, color="type", nbins=40, barmode="overlay", opacity=0.65,
                           color_discrete_map=u.COLORES, log_x=logx)
        st.plotly_chart(u.estilo(fig, f"Histograma · {var}"), width="stretch")
    with b:
        fig = px.box(datos, x="type", y=col, color="type", color_discrete_map=u.COLORES, log_y=logx)
        fig.update_layout(showlegend=False)
        st.plotly_chart(u.estilo(fig, f"Boxplot por tipo · {var}"), width="stretch")
    r = datos.groupby("type")[col].describe()[["count", "mean", "50%", "min", "max"]].rename(
        columns={"count": "n", "mean": "promedio", "50%": "mediana", "min": "mín", "max": "máx"})
    st.dataframe(r.round(2), width="stretch")
    if var == "Año de estreno":
        st.warning("La distribución por año es **plana (≈2.000 títulos/año)**: es una característica del extracto, "
                   "no una tendencia de negocio. No debe leerse como crecimiento.")
    if logx:
        st.caption("Escala logarítmica: la distribución es muy asimétrica (pocos títulos concentran casi todo el valor).")

# -------------------------------------------------------------- Relaciones ----
with tabs[2]:
    st.subheader("¿Qué variables se mueven juntas?")
    base = df.dropna(subset=["calificacion"])[["popularity", "popularity_pct", "calificacion", "vote_count", "release_year", "type"]]
    tipo = st.radio("Calcular correlación para", ["Movie", "TV Show"], horizontal=True)
    sub = base[base["type"] == tipo].drop(columns="type")
    if len(sub) < 30:
        st.warning("Muy pocos títulos con estos filtros para correlacionar.")
    else:
        corr = sub.corr(method="spearman").round(2)
        corr.index = corr.columns = ["Popularidad", "Popularidad (percentil)", "Calificación", "Votos", "Año"]
        fig = px.imshow(corr, text_auto=True, zmin=-1, zmax=1, color_continuous_scale="RdBu_r", aspect="auto")
        st.plotly_chart(u.estilo(fig, f"Correlación de Spearman · {tipo}", 420), width="stretch")
    st.caption("Spearman: robusta a valores extremos y a escalas distintas. Se calcula por tipo porque películas y series "
               "tienen escalas de popularidad diferentes. **Correlación ≠ causalidad.**")

# --------------------------------------------------------------- Anomalías ----
with tabs[3]:
    st.subheader("¿Qué datos son inusuales?")
    st.markdown("Regla del rango intercuartílico (IQR) sobre el **ROI** de las películas con datos financieros.")
    fin = financiero[financiero["type"].isin(f["tipos"])] if "type" in financiero.columns else financiero
    lr = np.log10(fin["roi"])
    q1, q3 = lr.quantile([0.25, 0.75])
    lim = q3 + 1.5 * (q3 - q1)
    fin = fin.assign(anomalo=lr > lim)
    a, b = st.columns([3, 2])
    with a:
        fig = px.strip(fin, x="roi", y="presupuesto_realista", color="anomalo", log_x=True,
                       hover_data=["title", "budget", "revenue"],
                       color_discrete_map={True: u.NARANJA, False: u.AZUL})
        fig.update_yaxes(title="Presupuesto realista (≥ USD 10.000)")
        st.plotly_chart(u.estilo(fig, "ROI por película (escala log) · anomalías en naranja", 380), width="stretch")
    with b:
        st.metric("Películas con ROI atípico", u.n(fin["anomalo"].sum()))
        st.metric("ROI mínimo para ser atípico", f"{u.d(10 ** lim, 0)}x")
        top = fin[fin["anomalo"]].sort_values("roi", ascending=False).head(8)[["title", "budget", "roi"]]
        st.dataframe(top.rename(columns={"title": "Película", "budget": "Presupuesto", "roi": "ROI (x)"}),
                     hide_index=True, width="stretch",
                     column_config={"ROI (x)": st.column_config.NumberColumn(format="%.0f"),
                                    "Presupuesto": st.column_config.NumberColumn(format="$%d")})
    st.caption("Un ROI atípico puede ser un éxito real (bajo presupuesto, gran taquilla) **o un dato mal cargado**. "
               "Validar con fuente antes de basar una decisión de adquisición en él.")
