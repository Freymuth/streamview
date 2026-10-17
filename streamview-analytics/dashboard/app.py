"""
StreamView Analytics - EA1
Dashboard interactivo (Streamlit + Plotly) sobre el catálogo oficial de
películas y series (netflix_movies_detailed_up_to_2025.csv /
netflix_tv_shows_detailed_up_to_2025.csv).

Ejecutar desde la raíz del proyecto: streamlit run dashboard/app.py
"""

import sys
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.append(".")
from src.data.clean_data import cargar_datos_crudos, limpiar_datasets, unificar_catalogo, aplicar_reglas_negocio

st.set_page_config(page_title="StreamView Analytics", layout="wide")

COLORS = {"Movie": "#2563EB", "TV Show": "#F97316"}


@st.cache_data
def cargar_catalogo():
    """Carga el catálogo ya procesado si existe; si no, corre el pipeline
    completo de limpieza y reglas de negocio sobre los datos oficiales."""
    try:
        catalogo = pd.read_csv("data/processed/catalogo_limpio.csv")
        financiero = pd.read_csv("data/processed/catalogo_financiero.csv")
    except FileNotFoundError:
        tv, mv = cargar_datos_crudos()
        tv, mv = limpiar_datasets(tv, mv, resumen=[])
        catalogo = unificar_catalogo(tv, mv)
        catalogo, financiero = aplicar_reglas_negocio(catalogo, resumen=[])
    return catalogo, financiero


catalogo, financiero = cargar_catalogo()

# ---------------------------------------------------------------------------
# SIDEBAR - FILTROS DINÁMICOS (requerimiento del caso)
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros de exploración")

tipos = st.sidebar.multiselect(
    "Tipo de contenido:", options=["Movie", "TV Show"], default=["Movie", "TV Show"]
)

anio_min, anio_max = int(catalogo["release_year"].min()), int(catalogo["release_year"].max())
rango_anios = st.sidebar.slider(
    "Año de estreno:", min_value=anio_min, max_value=anio_max, value=(anio_min, anio_max)
)

generos_disponibles = sorted(
    set(g for lista in catalogo["genres"].str.split(", ") for g in lista if g != "Desconocido")
)
genero_sel = st.sidebar.selectbox("Género:", options=["Todos"] + generos_disponibles)

idiomas_disponibles = sorted(catalogo["language"].dropna().unique())
idioma_sel = st.sidebar.selectbox("Idioma:", options=["Todos"] + idiomas_disponibles)

# Aplicar filtros
df = catalogo[
    catalogo["type"].isin(tipos)
    & catalogo["release_year"].between(*rango_anios)
]
if genero_sel != "Todos":
    df = df[df["genres"].str.contains(genero_sel, na=False)]
if idioma_sel != "Todos":
    df = df[df["language"] == idioma_sel]

fin_filtrado = financiero[financiero["show_id"].isin(df["show_id"])]

# ---------------------------------------------------------------------------
# ENCABEZADO Y KPIs
# ---------------------------------------------------------------------------
st.title("🎬 StreamView Analytics — Catálogo Audiovisual")
st.caption(
    f"Periodo analizado: {rango_anios[0]}–{rango_anios[1]} · "
    f"{len(df):,} títulos con los filtros actuales".replace(",", ".")
)

generos_expl = df.assign(genero=df["genres"].str.split(", ")).explode("genero")
generos_expl = generos_expl[generos_expl["genero"] != "Desconocido"]
paises_expl = df.assign(pais=df["country"].str.split(", ")).explode("pais")
paises_expl = paises_expl[paises_expl["pais"] != "Desconocido"]

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total contenidos", f"{len(df):,}".replace(",", "."))
k2.metric("Películas", f"{(df['type'] == 'Movie').sum():,}".replace(",", "."))
k3.metric("Series", f"{(df['type'] == 'TV Show').sum():,}".replace(",", "."))
k4.metric("Países representados", paises_expl["pais"].nunique())
k5.metric("Popularidad promedio", round(df["popularity"].mean(), 1) if len(df) else "—")
k6.metric("Calificación promedio", round(df["vote_average"].mean(), 2) if len(df) else "—")

st.divider()

tab_catalogo, tab_popularidad, tab_temporal, tab_financiero = st.tabs(
    ["📚 Catálogo", "⭐ Popularidad y valoración", "📈 Evolución temporal", "💰 Financiero"]
)

# ---------------------------------------------------------------------------
# TAB 1: CARACTERIZACIÓN Y ESTRUCTURA DEL CATÁLOGO
# ---------------------------------------------------------------------------
with tab_catalogo:
    col1, col2 = st.columns(2)

    with col1:
        conteo_tipo = df["type"].value_counts().reset_index()
        conteo_tipo.columns = ["type", "cantidad"]
        fig = px.pie(
            conteo_tipo, names="type", values="cantidad", hole=0.45,
            title="Distribución: películas vs series", color="type",
            color_discrete_map=COLORS,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_generos = generos_expl["genero"].value_counts().head(10).reset_index()
        top_generos.columns = ["genero", "cantidad"]
        fig = px.bar(
            top_generos.sort_values("cantidad"), x="cantidad", y="genero", orientation="h",
            title="Top 10 géneros predominantes",
            labels={"cantidad": "Cantidad de títulos", "genero": "Género"},
            color="cantidad", color_continuous_scale="Blues",
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        top_paises = paises_expl["pais"].value_counts().head(10).reset_index()
        top_paises.columns = ["pais", "cantidad"]
        fig = px.bar(
            top_paises.sort_values("cantidad"), x="cantidad", y="pais", orientation="h",
            title="Top 10 países de producción",
            labels={"cantidad": "Cantidad de títulos", "pais": "País"},
            color="cantidad", color_continuous_scale="Oranges",
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        top_idiomas = df["language"].value_counts().head(10).reset_index()
        top_idiomas.columns = ["idioma", "cantidad"]
        fig = px.bar(
            top_idiomas.sort_values("cantidad"), x="cantidad", y="idioma", orientation="h",
            title="Top 10 idiomas del catálogo",
            labels={"cantidad": "Cantidad de títulos", "idioma": "Idioma"},
            color="cantidad", color_continuous_scale="Greens",
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 2: POPULARIDAD Y VALORACIÓN
# ---------------------------------------------------------------------------
with tab_popularidad:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(
            df, x="type", y="popularity_norm", color="type", color_discrete_map=COLORS,
            title="Comparativa de popularidad normalizada",
            labels={"popularity_norm": "Popularidad normalizada (0-1)", "type": "Tipo"},
            points=False,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        muestra = df.sample(min(3000, len(df)), random_state=42) if len(df) else df
        fig = px.scatter(
            muestra, x="popularity", y="vote_average", color="type", color_discrete_map=COLORS,
            title="Popularidad vs. calificación de la audiencia",
            labels={"popularity": "Popularidad", "vote_average": "Calificación promedio"},
            opacity=0.5, log_x=True,
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 3: ANÁLISIS TEMPORAL
# ---------------------------------------------------------------------------
with tab_temporal:
    evolucion = df.groupby(["release_year", "type"]).size().reset_index(name="cantidad")
    fig = px.line(
        evolucion, x="release_year", y="cantidad", color="type", color_discrete_map=COLORS,
        markers=True, title="Evolución histórica de estrenos por año",
        labels={"release_year": "Año de estreno", "cantidad": "Cantidad de títulos", "type": "Tipo"},
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 4: ANÁLISIS FINANCIERO (solo películas con budget/revenue conocidos,
# regla de negocio del caso)
# ---------------------------------------------------------------------------
with tab_financiero:
    st.info(
        "Presupuesto e ingresos solo están disponibles para películas, y únicamente "
        "se incluyen aquí los títulos con ambos datos conocidos (regla de negocio del caso)."
    )
    if len(fin_filtrado) == 0:
        st.warning("No hay títulos con datos financieros completos bajo los filtros actuales.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(
                fin_filtrado, x="budget", y="revenue", color="vote_average",
                title="Presupuesto vs. ingresos",
                labels={"budget": "Presupuesto (USD)", "revenue": "Ingresos (USD)", "vote_average": "Calificación"},
                hover_data=["title"], log_x=True, log_y=True, color_continuous_scale="Viridis",
            )
            max_val = max(fin_filtrado["budget"].max(), fin_filtrado["revenue"].max())
            fig.add_shape(type="line", x0=1, y0=1, x1=max_val, y1=max_val, line=dict(color="red", dash="dash"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            top_roi = fin_filtrado.sort_values("roi", ascending=False).head(15)
            fig = px.bar(
                top_roi.sort_values("roi"), x="roi", y="title", orientation="h",
                title="Top 15 títulos con mayor retorno de inversión (ROI)",
                labels={"roi": "ROI (veces lo invertido)", "title": "Título"},
                color="roi", color_continuous_scale="Tealgrn",
            )
            fig.update_layout(coloraxis_showscale=False, height=500)
            st.plotly_chart(fig, use_container_width=True)
