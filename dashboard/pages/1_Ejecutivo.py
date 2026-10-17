"""
StreamView Analytics - EA2
Dashboard EJECUTIVO — Directorio y Gerencia General.

Objetivo: comprender rápidamente el estado del catálogo y apoyar decisiones de
inversión y crecimiento. Responde: ¿cómo evolucionó el catálogo? ¿qué géneros,
países e idiomas predominan?
"""

import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.append(".")
from dashboard import utils as u  # noqa: E402
from src.common import explotar  # noqa: E402

st.set_page_config(page_title="Ejecutivo · StreamView", page_icon="📊", layout="wide")

catalogo, financiero = u.cargar_datos()
f = u.sidebar_filtros(catalogo, analitico=False)
df = u.aplicar_filtros(catalogo, f)

st.title("📊 Dashboard Ejecutivo")
st.caption("Directorio y Gerencia General · " + u.alcance(f, len(df)))

if df.empty:
    st.warning("No hay títulos con los filtros actuales. Amplía el rango de años o el tipo de contenido.")
    st.stop()

generos = explotar(df, "lista_generos", "genero")
paises = explotar(df, "lista_paises", "pais")

# ---------------------------------------------------------------- KPIs ----
a, b, c, e = st.columns(4)
a.metric("Total de contenidos", u.n(len(df)))
b.metric("Películas", u.n((df["type"] == "Movie").sum()))
c.metric("Series", u.n((df["type"] == "TV Show").sum()))
e.metric("Países representados", u.n(paises["pais"].nunique()))
g, h, i, j = st.columns(4)
g.metric("Idiomas disponibles", u.n(df["idioma_nombre"].nunique()))
h.metric("Géneros", u.n(generos["genero"].nunique()))
i.metric("Popularidad promedio", u.d(df["popularity"].mean(), 1), help="Índice relativo de TMDB; no representa reproducciones.")
j.metric(
    "Calificación promedio (0-10)",
    u.d(df["calificacion"].mean(), 2) if df["calificacion"].notna().any() else "—",
    help="Promedio solo de títulos con 10 o más votos (con menos, la nota no es confiable).",
)

st.divider()

# ----------------------------------------- Evolución + película vs serie ----
col1, col2 = st.columns([2, 1])
with col1:
    estrenos = df.groupby("release_year").size()
    incorporacion = df.dropna(subset=["anio_incorporacion"]).groupby("anio_incorporacion").size()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=estrenos.index, y=estrenos.values, name="Estrenos", mode="lines",
                             fill="tozeroy", line=dict(color=u.AZUL), opacity=0.55))
    fig.add_trace(go.Scatter(x=incorporacion.index, y=incorporacion.values, name="Incorporación a la plataforma",
                             mode="lines", fill="tozeroy", line=dict(color=u.NARANJA), opacity=0.45))
    fig.update_xaxes(title="Año", dtick=1 if (f["anios"][1] - f["anios"][0]) <= 20 else None)
    fig.update_yaxes(title="Títulos por año")
    st.plotly_chart(u.estilo(fig, "Evolución del catálogo: estrenos e incorporación por año"), width="stretch")
    if len(estrenos) > 3 and estrenos.std() / estrenos.mean() < 0.1:
        st.caption(
            "⚠️ Los datos entregados contienen una cantidad casi idéntica de títulos por año "
            "(≈2.000). La ausencia de tendencia es una característica del extracto, no un hallazgo de negocio."
        )

with col2:
    tipo = df["type"].value_counts().reset_index()
    tipo.columns = ["type", "titulos"]
    fig = px.bar(tipo, x="type", y="titulos", color="type", color_discrete_map=u.COLORES, text="titulos",
                 labels={"type": "", "titulos": "Títulos"})
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(showlegend=False)
    fig.update_yaxes(range=[0, tipo["titulos"].max() * 1.15])
    st.plotly_chart(u.estilo(fig, "Películas vs. series"), width="stretch")

# -------------------------------------------------- Mapa + top países ------
col1, col2 = st.columns([3, 2])
tp = u.tabla_paises(df)
with col1:
    mapa = tp.dropna(subset=["iso3"])
    fig = px.choropleth(
        mapa, locations="iso3", color="titulos", hover_name="pais",
        hover_data={"iso3": False, "titulos": ":,"}, color_continuous_scale="Blues",
        labels={"titulos": "Títulos"},
    )
    fig.update_geos(showframe=False, showcoastlines=False, projection_type="natural earth")
    fig.update_layout(coloraxis_colorbar=dict(title="Títulos", thickness=12))
    st.plotly_chart(u.estilo(fig, "Producciones por país (mapa)", alto=420), width="stretch")
with col2:
    top = tp.head(10).sort_values("titulos")
    fig = px.bar(top, x="titulos", y="pais", orientation="h", labels={"titulos": "Títulos", "pais": ""},
                 text="titulos", color_discrete_sequence=[u.AZUL])
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False)
    st.plotly_chart(u.estilo(fig, "Top 10 países con más producciones", alto=420), width="stretch")

# ------------------------------------------------ Géneros + idiomas --------
col1, col2 = st.columns(2)
with col1:
    tg = u.tabla_generos(df).head(10).sort_values("titulos")
    fig = px.bar(tg, x="titulos", y="genero", orientation="h", labels={"titulos": "Títulos", "genero": ""},
                 text="titulos", color_discrete_sequence=[u.AZUL])
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False)
    st.plotly_chart(u.estilo(fig, "Top 10 géneros"), width="stretch")
with col2:
    ti = df["idioma_nombre"].value_counts().head(10).reset_index()
    ti.columns = ["idioma", "titulos"]
    ti = ti.sort_values("titulos")
    fig = px.bar(ti, x="titulos", y="idioma", orientation="h", labels={"titulos": "Títulos", "idioma": ""},
                 text="titulos", color_discrete_sequence=[u.AZUL])
    fig.update_traces(texttemplate="%{text:,}", textposition="outside", cliponaxis=False)
    st.plotly_chart(u.estilo(fig, "Top 10 idiomas"), width="stretch")

# --------------------------------------------------- Lectura ejecutiva -----
st.divider()
top_g = u.tabla_generos(df).iloc[0]
top_p = tp.iloc[0]
top_i = df["idioma_nombre"].value_counts()
pct_tipo = df["type"].value_counts(normalize=True)
st.subheader("Lectura ejecutiva")
st.markdown(
    f"""
- **¿Cómo evolucionó el catálogo?** Entre {f['anios'][0]} y {f['anios'][1]} el extracto reúne
  {u.n(len(df))} títulos; la serie anual de estrenos va de {u.n(estrenos.min())} a {u.n(estrenos.max())} títulos por año.
- **¿Qué predomina?** Género **{top_g['genero']}** ({u.n(top_g['titulos'])} títulos),
  país **{top_p['pais']}** ({u.n(top_p['titulos'])}) e idioma **{top_i.index[0]}**
  ({u.d(100 * top_i.iloc[0] / len(df), 1)}% del catálogo).
- **Composición:** {u.d(100 * pct_tipo.get('Movie', 0), 1)}% películas y {u.d(100 * pct_tipo.get('TV Show', 0), 1)}% series.
"""
)
st.caption("Un título puede tener varios géneros o países: en esos gráficos se cuenta una vez por cada uno.")
