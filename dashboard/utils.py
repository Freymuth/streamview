"""
StreamView Analytics - EA2
Capa compartida de los dashboards Streamlit: carga de datos, filtros,
formato y estilo gráfico consistente.
"""

import os
import sys

import pandas as pd
import streamlit as st

sys.path.append(".")
from src.common import DESCONOCIDOS, explotar, pais_a_iso3, separar  # noqa: E402

CAT = "data/processed/catalogo_limpio.csv"
FIN = "data/processed/catalogo_financiero.csv"

# Paleta única (accesible: azul/naranja distinguibles para daltonismo)
COLORES = {"Movie": "#2563EB", "TV Show": "#F97316"}
AZUL, NARANJA, GRIS = "#2563EB", "#F97316", "#6B7280"
PLANTILLA = "plotly_white"


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Cargando catálogo…")
def cargar_datos():
    """Devuelve (catalogo, financiero). Si no existe data/processed/, corre el
    pipeline de limpieza sobre los datos oficiales."""
    if not (os.path.exists(CAT) and os.path.exists(FIN)):
        from src.data.clean_data import main as correr_pipeline

        correr_pipeline()
    catalogo = pd.read_csv(CAT, parse_dates=["date_added"])
    financiero = pd.read_csv(FIN, parse_dates=["date_added"])
    for df in (catalogo, financiero):
        df["lista_generos"] = df["genres"].map(separar)
        df["lista_paises"] = df["country"].map(separar)
        df["lista_directores"] = df["director"].map(separar)
        df["lista_actores"] = df["cast"].map(separar)
    return catalogo, financiero


# ---------------------------------------------------------------------------
# Formato
# ---------------------------------------------------------------------------
def n(x):
    """Entero con separador de miles chileno (punto)."""
    return f"{int(x):,}".replace(",", ".")


def d(x, dec=1):
    """Decimal con coma."""
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def usd_m(x):
    """USD en millones: 'USD 125.430 M'."""
    return f"USD {n(round(x / 1e6))} M"


def estilo(fig, titulo, alto=380):
    fig.update_layout(
        template=PLANTILLA,
        title=dict(text=titulo, font=dict(size=15)),
        height=alto,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=-0.15),
    )
    return fig


# ---------------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------------
def sidebar_filtros(catalogo, analitico):
    """Dibuja los filtros en la barra lateral y devuelve sus valores."""
    sb = st.sidebar
    sb.header("Filtros")
    f = {}
    f["tipos"] = sb.multiselect("Tipo de contenido", ["Movie", "TV Show"], default=["Movie", "TV Show"])
    amin, amax = int(catalogo["release_year"].min()), int(catalogo["release_year"].max())
    f["anios"] = sb.slider("Rango de años (estreno)", amin, amax, (amin, amax))
    generos = sorted({g for l in catalogo["lista_generos"] for g in l})
    f["generos"] = sb.multiselect("Género", generos, placeholder="Todos")

    f["paises"], f["idiomas"], f["calif"] = [], [], (0.0, 10.0)
    if analitico:
        paises = sorted({p for l in catalogo["lista_paises"] for p in l})
        f["paises"] = sb.multiselect("País", paises, placeholder="Todos")
        idiomas = sorted(catalogo["idioma_nombre"].dropna().unique())
        f["idiomas"] = sb.multiselect("Idioma", idiomas, placeholder="Todos")
        f["calif"] = sb.slider("Rango de calificación (0-10)", 0.0, 10.0, (0.0, 10.0), step=0.5)
        sb.selectbox(
            "Clasificación etaria",
            ["No disponible en los datos"],
            disabled=True,
            help="El campo 'rating' del extracto es numérico y es idéntico a vote_average "
            "(100% de coincidencia), por lo que NO contiene clasificación por edad "
            "(TV-MA, PG-13...). Ver docs/ea2_justificacion_graficos.md, sección Limitaciones.",
        )
    return f


def aplicar_filtros(df, f):
    out = df[df["type"].isin(f["tipos"]) & df["release_year"].between(*f["anios"])]
    if f["generos"]:
        sel = set(f["generos"])
        out = out[out["lista_generos"].map(lambda l: bool(sel & set(l)))]
    if f["paises"]:
        sel = set(f["paises"])
        out = out[out["lista_paises"].map(lambda l: bool(sel & set(l)))]
    if f["idiomas"]:
        out = out[out["idioma_nombre"].isin(f["idiomas"])]
    if f["calif"] != (0.0, 10.0):
        out = out[out["calificacion"].between(*f["calif"])]
    return out


def alcance(f, total):
    """Texto de período y alcance (regla de negocio 7)."""
    partes = [f"Período: {f['anios'][0]}–{f['anios'][1]}", " + ".join(f["tipos"]) or "sin tipo"]
    if f["generos"]:
        partes.append("Género: " + ", ".join(f["generos"][:3]) + ("…" if len(f["generos"]) > 3 else ""))
    if f["paises"]:
        partes.append("País: " + ", ".join(f["paises"][:3]) + ("…" if len(f["paises"]) > 3 else ""))
    if f.get("idiomas"):
        partes.append("Idioma: " + ", ".join(f["idiomas"][:3]) + ("…" if len(f["idiomas"]) > 3 else ""))
    if f.get("calif") and f["calif"] != (0.0, 10.0):
        partes.append(f"Calificación {f['calif'][0]:g}–{f['calif'][1]:g}")
    partes.append(f"{n(total)} títulos")
    return " · ".join(partes)


# ---------------------------------------------------------------------------
# Agregaciones reutilizadas
# ---------------------------------------------------------------------------
def tabla_generos(df):
    g = explotar(df, "lista_generos", "genero")
    t = g.groupby("genero").agg(
        titulos=("uid", "count"), n_calif=("calificacion", "count"), calificacion=("calificacion", "mean"),
        popularidad=("popularity", "mean"), popularidad_pct=("popularity_pct", "mean"),
    )
    return t.reset_index().sort_values("titulos", ascending=False)


def tabla_paises(df):
    p = explotar(df, "lista_paises", "pais")
    t = p.groupby("pais").agg(
        titulos=("uid", "count"), n_calif=("calificacion", "count"),
        calificacion=("calificacion", "mean"), popularidad=("popularity", "mean"),
    )
    t = t.reset_index()
    t["iso3"] = t["pais"].map(pais_a_iso3)
    return t.sort_values("titulos", ascending=False)


def generos_a_priorizar(tg, min_titulos=100, k=5):
    """Puntaje = promedio de los percentiles de popularidad relativa y calificación.

    Se usa popularity_pct (percentil dentro de cada tipo) porque la popularidad de series y
    películas está en escalas distintas (regla de negocio 2: comparar solo variables equivalentes).
    """
    t = tg[tg["n_calif"] >= min_titulos].copy()
    if t.empty:
        return t
    t["puntaje"] = (t["popularidad_pct"].rank(pct=True) + t["calificacion"].rank(pct=True)) / 2
    return t.sort_values("puntaje", ascending=False).head(k)


def paises_oportunidad(tp, min_titulos=20, k=10):
    """Calificación alta (≥ percentil 75) con oferta aún baja (≤ mediana de títulos).
    El mínimo se exige sobre títulos con calificación válida (n_calif), que son los que entran al promedio."""
    t = tp[tp["n_calif"] >= min_titulos].dropna(subset=["calificacion"])
    if len(t) < 4:
        return t.iloc[0:0]
    sel = t[(t["calificacion"] >= t["calificacion"].quantile(0.75)) & (t["titulos"] <= t["titulos"].median())]
    return sel.sort_values("calificacion", ascending=False).head(k)


def interpretar_rho(rho):
    a = abs(rho)
    fuerza = "prácticamente nula" if a < 0.1 else "débil" if a < 0.3 else "moderada" if a < 0.5 else "fuerte"
    signo = "positiva" if rho > 0 else "negativa"
    return fuerza if a < 0.1 else f"{fuerza} {signo}"


def incrustar_html(html, alto):
    """Incrusta HTML+JS propio (visualización D3). Usa st.iframe en Streamlit
    recientes y components.html como respaldo en versiones anteriores."""
    if hasattr(st, "iframe"):
        st.iframe(html, height=alto)
    else:
        import streamlit.components.v1 as components

        components.html(html, height=alto)


def correlaciones_por_tipo(df):
    """Spearman popularidad–calificación por tipo (mezclar tipos mezcla escalas distintas)."""
    cn = df.dropna(subset=["calificacion"])
    out = {}
    for tipo in ["Movie", "TV Show"]:
        x = cn[cn["type"] == tipo]
        if len(x) > 30:
            out[tipo] = x[["popularity", "calificacion"]].corr(method="spearman").iloc[0, 1]
    return out
