"""
StreamView Analytics - EA2
Dashboard ANALÍTICO — Gerencia de Contenidos y Adquisición (con análisis financiero).

Responde: ¿qué géneros priorizar? ¿qué países son oportunidad? ¿qué películas fueron
exitosas con presupuestos reducidos? ¿existe relación entre popularidad y calificación?
"""

import sys

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

sys.path.append(".")
from dashboard import utils as u  # noqa: E402
from src.common import explotar  # noqa: E402
from src.d3_treemap import construir_html_treemap  # noqa: E402

st.set_page_config(page_title="Analítico · StreamView", page_icon="🔎", layout="wide")

catalogo, financiero = u.cargar_datos()
f = u.sidebar_filtros(catalogo, analitico=True)

with st.sidebar.expander("Umbrales de confiabilidad", expanded=False):
    min_votos = st.slider("Mín. de votos (Top mejor evaluados)", 0, 5000, 500, step=50,
                          help="Evita que títulos con pocos votos dominen el ranking.")
    min_titulos_pais = st.slider("Mín. de títulos por país (mapa y oportunidades)", 1, 200, 20,
                                 help="Un promedio de pocos títulos no es confiable.")
    pct_presupuesto = st.slider("«Presupuesto reducido» = por debajo del percentil", 5, 50, 25, step=5)
    roi_min = st.slider("ROI mínimo para considerar «éxito»", 1.0, 20.0, 3.0, step=0.5)

df = u.aplicar_filtros(catalogo, f)
st.title("🔎 Dashboard Analítico")
st.caption("Gerencia de Contenidos y Adquisición · " + u.alcance(f, len(df)))

if df.empty:
    st.warning("No hay títulos con los filtros actuales. Relaja algún filtro en la barra lateral.")
    st.stop()

# Financiero: solo películas del filtro actual con budget y revenue informados
fin = financiero[financiero["uid"].isin(df["uid"])]
n_peliculas = int((df["type"] == "Movie").sum())

tabs = st.tabs(["⭐ Popularidad y calificación", "🎭 Géneros", "🌍 Países", "🎬 Directores y actores",
                "💰 Financiero", "🧭 Conclusiones"])

# =========================================================== TAB 1 =========
with tabs[0]:
    con_nota = df.dropna(subset=["calificacion"])
    col1, col2 = st.columns([3, 2])
    with col1:
        muestra = con_nota.sample(min(2500, len(con_nota)), random_state=42) if len(con_nota) else con_nota
        fig = px.scatter(
            muestra, x="popularity", y="calificacion", size="vote_count", color="type", size_max=26,
            color_discrete_map=u.COLORES, log_x=True, opacity=0.55, hover_name="title",
            labels={"popularity": "Popularidad (escala log)", "calificacion": "Calificación (0-10)",
                    "vote_count": "Votos", "type": "Tipo"},
        )
        st.plotly_chart(u.estilo(fig, "Popularidad vs. calificación (tamaño = cantidad de votos)", alto=440),
                        width="stretch")
        st.caption(f"Muestra aleatoria de {u.n(len(muestra))} de {u.n(len(con_nota))} títulos con ≥10 votos.")
    with col2:
        rhos = u.correlaciones_por_tipo(df)
        if rhos:
            st.markdown("**Correlación popularidad–calificación (Spearman)**")
            cols = st.columns(len(rhos))
            for cc, (tipo, rho) in zip(cols, rhos.items()):
                cc.metric("Películas" if tipo == "Movie" else "Series", u.d(rho, 2), help=f"Relación {u.interpretar_rho(rho)}. De −1 a 1; cerca de 0 = sin relación.")
            st.caption("Se calcula por separado porque películas y series tienen escalas de popularidad distintas.")
        top = con_nota[con_nota["vote_count"] >= min_votos].sort_values(["calificacion", "vote_count"], ascending=False).head(10)
        if top.empty:
            st.info(f"Ningún título alcanza {u.n(min_votos)} votos con estos filtros.")
        else:
            top = top.sort_values("calificacion")
            top["etiqueta"] = top["title"].str.slice(0, 32)
            fig = px.bar(top, x="calificacion", y="etiqueta", orientation="h", color="type", color_discrete_map=u.COLORES,
                         text="calificacion", hover_data={"vote_count": ":,", "etiqueta": False},
                         labels={"calificacion": "Calificación", "etiqueta": "", "type": "Tipo"})
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", cliponaxis=False)
            fig.update_xaxes(range=[0, 10.5])
            st.plotly_chart(u.estilo(fig, f"Top 10 mejor evaluados (≥ {u.n(min_votos)} votos)", alto=440),
                            width="stretch")

# =========================================================== TAB 2 =========
with tabs[1]:
    tg = u.tabla_generos(df)
    col1, col2 = st.columns([2, 3])
    with col1:
        top = tg.head(12).sort_values("titulos")
        fig = make_subplots(rows=1, cols=2, shared_yaxes=True, horizontal_spacing=0.04,
                            subplot_titles=("Popularidad promedio", "Calificación promedio"))
        fig.add_trace(go.Bar(x=top["popularidad"], y=top["genero"], orientation="h", marker_color=u.NARANJA,
                             text=top["popularidad"].round(1), textposition="outside", cliponaxis=False,
                             showlegend=False), row=1, col=1)
        fig.add_trace(go.Bar(x=top["calificacion"], y=top["genero"], orientation="h", marker_color=u.AZUL,
                             text=top["calificacion"].round(2), textposition="outside", cliponaxis=False,
                             showlegend=False), row=1, col=2)
        fig.update_xaxes(range=[0, top["popularidad"].max() * 1.25], row=1, col=1)
        fig.update_xaxes(range=[0, 10.5], row=1, col=2)
        st.plotly_chart(u.estilo(fig, "Popularidad y calificación por género (12 más voluminosos)", alto=460),
                        width="stretch")
    with col2:
        motor = st.radio("Motor del treemap", ["D3.js", "Plotly"], horizontal=True,
                         help="D3 recibe los datos desde Python como JSON. Si no hay internet, usa Plotly.")
        if motor == "D3.js":
            u.incrustar_html(construir_html_treemap(tg, ancho=760, alto=400), 470)
        else:
            fig = px.treemap(tg, path=["genero"], values="titulos", color="calificacion",
                             color_continuous_scale="Blues", labels={"calificacion": "Calificación prom."})
            st.plotly_chart(u.estilo(fig, "Géneros por volumen (tamaño = títulos, color = calificación)", alto=440),
                            width="stretch")
    st.caption("Películas y series tienen escalas de popularidad distintas (promedio ≈20 vs ≈65): para comparar géneros de forma justa, filtra por tipo. "
               "El promedio también es sensible a valores extremos.")

# =========================================================== TAB 3 =========
with tabs[2]:
    tp = u.tabla_paises(df)
    metrica = st.radio("Métrica del mapa", ["Calificación promedio", "Popularidad promedio"], horizontal=True)
    col_m = "calificacion" if metrica.startswith("Calif") else "popularidad"
    base_n = "n_calif" if col_m == "calificacion" else "titulos"
    confiables = tp[tp[base_n] >= min_titulos_pais].dropna(subset=["iso3", col_m])
    col1, col2 = st.columns([3, 2])
    with col1:
        if confiables.empty:
            st.info(f"Ningún país tiene ≥ {min_titulos_pais} títulos válidos con estos filtros. Baja el umbral.")
        else:
            fig = px.choropleth(confiables, locations="iso3", color=col_m, hover_name="pais",
                                hover_data={"iso3": False, "titulos": ":,", "n_calif": ":,", col_m: ":.2f"},
                                color_continuous_scale="Blues", labels={col_m: metrica, "titulos": "Títulos", "n_calif": "Títulos con calificación válida"})
            fig.update_geos(showframe=False, showcoastlines=False, projection_type="natural earth")
            fig.update_layout(coloraxis_colorbar=dict(title="", thickness=12))
            st.plotly_chart(u.estilo(fig, f"{metrica} por país (países con ≥ {min_titulos_pais} títulos válidos)", alto=430),
                            width="stretch")
            st.caption(f"{u.n(len(confiables))} de {u.n(len(tp))} países cumplen el mínimo de títulos; "
                       "el resto se excluye por no ser confiable."
                       + (" Para calificación se cuentan solo títulos con ≥10 votos." if col_m == "calificacion" else ""))
    with col2:
        top = confiables.sort_values(col_m, ascending=False).head(10).sort_values(col_m)
        if not top.empty:
            fig = px.bar(top, x=col_m, y="pais", orientation="h", text=col_m, color_discrete_sequence=[u.AZUL],
                         labels={col_m: metrica, "pais": ""}, hover_data={"titulos": ":,"})
            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", cliponaxis=False)
            st.plotly_chart(u.estilo(fig, f"Top 10 países por {metrica.lower()}", alto=430), width="stretch")

# =========================================================== TAB 4 =========
with tabs[3]:
    col1, col2 = st.columns(2)
    for col, lista, nombre, titulo in [
        (col1, "lista_directores", "director", "Top 10 directores por cantidad de contenidos"),
        (col2, "lista_actores", "actor", "Top 10 actores por cantidad de contenidos"),
    ]:
        with col:
            t = explotar(df, lista, nombre).groupby(nombre).agg(
                titulos=("uid", "count"), calificacion=("calificacion", "mean")).reset_index()
            t = t.sort_values("titulos", ascending=False).head(10).sort_values("titulos")
            fig = px.bar(t, x="titulos", y=nombre, orientation="h", text="titulos", color_discrete_sequence=[u.AZUL],
                         hover_data={"calificacion": ":.2f"}, labels={"titulos": "Títulos", nombre: ""})
            fig.update_traces(textposition="outside", cliponaxis=False)
            st.plotly_chart(u.estilo(fig, titulo, alto=420), width="stretch")
    st.caption("Se excluyen los registros sin director/elenco informado (el 68% de las series no trae director).")

# =========================================================== TAB 5 =========
with tabs[4]:
    st.info(
        f"**Nota:** este análisis financiero incluye únicamente **películas con presupuesto e ingresos informados**: "
        f"{u.n(len(fin))} de {u.n(n_peliculas)} películas en el filtro actual "
        f"({u.d(100 * len(fin) / n_peliculas, 1) if n_peliculas else '0'}%). Las series no tienen estos datos."
    )
    if fin.empty:
        st.warning("No hay películas con datos financieros completos bajo los filtros actuales.")
    else:
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Películas analizadas", u.n(len(fin)))
        k2.metric("Presupuesto promedio", u.usd_m(fin["budget"].mean()))
        k3.metric("Total presupuesto", u.usd_m(fin["budget"].sum()))
        k4.metric("Total ingresos", u.usd_m(fin["revenue"].sum()))
        roi_total = fin["revenue"].sum() / fin["budget"].sum()
        k5.metric("ROI aproximado", f"{u.d(roi_total, 2)}x",
                  help=f"Ingresos totales / presupuesto total. ROI mediano por película: {u.d(fin['roi'].median(), 2)}x.")

        col1, col2 = st.columns(2)
        with col1:
            fig = px.scatter(fin, x="budget", y="revenue", color="calificacion", log_x=True, log_y=True,
                             hover_name="title", color_continuous_scale="Viridis", opacity=0.7,
                             labels={"budget": "Presupuesto (USD, log)", "revenue": "Ingresos (USD, log)",
                                     "calificacion": "Calificación"})
            lo, hi = fin["budget"].min(), max(fin["budget"].max(), fin["revenue"].max())
            fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", name="Punto de equilibrio (ROI = 1)",
                                     line=dict(color="#DC2626", dash="dash")))
            st.plotly_chart(u.estilo(fig, "Presupuesto vs. ingresos", alto=440), width="stretch")
            st.caption("Sobre la línea roja la película recuperó su presupuesto; bajo ella, no.")
        with col2:
            top = fin.sort_values("revenue", ascending=False).head(10).sort_values("revenue")
            top["ingresos_m"] = top["revenue"] / 1e6
            top["etiqueta"] = top["title"].str.slice(0, 32)
            fig = px.bar(top, x="ingresos_m", y="etiqueta", orientation="h", text="ingresos_m",
                         color_discrete_sequence=[u.AZUL], labels={"ingresos_m": "Ingresos (millones de USD)", "etiqueta": ""})
            fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", cliponaxis=False)
            st.plotly_chart(u.estilo(fig, "Top 10 películas por ingresos", alto=440), width="stretch")

        st.subheader("Éxitos con presupuesto reducido")
        corte = fin["budget"].quantile(pct_presupuesto / 100)
        exitos = fin[(fin["budget"] <= corte) & fin["presupuesto_realista"] & (fin["roi"] >= roi_min)]
        st.caption(f"Presupuesto reducido = ≤ USD {u.n(corte)} (percentil {pct_presupuesto}); éxito = ROI ≥ {u.d(roi_min, 1)}x; "
                   "se excluyen presupuestos menores a USD 10.000 por no ser realistas.")
        if exitos.empty:
            st.info("Ninguna película cumple esos criterios; relaja el ROI mínimo o el percentil en «Umbrales».")
        else:
            tabla = exitos.sort_values("roi", ascending=False).head(10)[
                ["title", "release_year", "budget", "revenue", "roi", "calificacion"]]
            st.dataframe(tabla, hide_index=True, width="stretch", column_config={
                "title": "Película", "release_year": st.column_config.NumberColumn("Año", format="%d"),
                "budget": st.column_config.NumberColumn("Presupuesto (USD)", format="%,d"),
                "revenue": st.column_config.NumberColumn("Ingresos (USD)", format="%,d"),
                "roi": st.column_config.NumberColumn("ROI (x)", format="%.1f"),
                "calificacion": st.column_config.NumberColumn("Calificación", format="%.1f")})
            st.caption(f"{u.n(len(exitos))} películas cumplen los criterios; se muestran las 10 de mayor ROI.")

# =========================================================== TAB 6 =========
with tabs[5]:
    st.caption("Lectura automática de los datos filtrados. Describe asociaciones, no causalidad.")
    tg = u.tabla_generos(df)
    tp = u.tabla_paises(df)

    st.markdown("#### 1) ¿Qué géneros priorizar?")
    pri = u.generos_a_priorizar(tg)
    if pri.empty:
        st.write("No hay géneros con volumen suficiente (≥100 títulos con calificación válida) bajo estos filtros.")
    else:
        st.write("Géneros con mejor combinación de popularidad relativa (percentil dentro de su tipo) y calificación, con ≥100 títulos con calificación válida:")
        st.dataframe(pri[["genero", "titulos", "popularidad_pct", "calificacion"]], hide_index=True, width="stretch",
                     column_config={"genero": "Género", "titulos": "Títulos",
                                    "popularidad_pct": st.column_config.NumberColumn("Popularidad relativa (percentil 0-1)", format="%.2f"),
                                    "calificacion": st.column_config.NumberColumn("Calificación prom.", format="%.2f")})

    st.markdown("#### 2) ¿Qué países son oportunidad?")
    opo = u.paises_oportunidad(tp, min_titulos=min_titulos_pais)
    if opo.empty:
        st.write("Ningún país cumple (calificación en el 25% superior con oferta bajo la mediana) con estos filtros.")
    else:
        st.write(f"Países con calificación alta (percentil 75 o más) y oferta bajo la mediana, con ≥ {min_titulos_pais} títulos con calificación válida:")
        st.dataframe(opo[["pais", "titulos", "n_calif", "calificacion", "popularidad"]], hide_index=True, width="stretch",
                     column_config={"pais": "País", "titulos": "Títulos", "n_calif": "Con calificación válida",
                                    "calificacion": st.column_config.NumberColumn("Calificación prom.", format="%.2f"),
                                    "popularidad": st.column_config.NumberColumn("Popularidad prom.", format="%.1f")})

    st.markdown("#### 3) ¿Qué películas fueron exitosas con presupuestos reducidos?")
    if fin.empty:
        st.write("Sin datos financieros bajo estos filtros.")
    else:
        corte = fin["budget"].quantile(pct_presupuesto / 100)
        ex = fin[(fin["budget"] <= corte) & fin["presupuesto_realista"] & (fin["roi"] >= roi_min)].sort_values("roi", ascending=False)
        if ex.empty:
            st.write("Ninguna película cumple los umbrales actuales.")
        else:
            lista = ", ".join(f"**{r.title}** ({u.d(r.roi, 1)}x)" for r in ex.head(5).itertuples())
            st.write(f"{u.n(len(ex))} películas con presupuesto ≤ USD {u.n(corte)} lograron ROI ≥ {u.d(roi_min, 1)}x. Las 5 mejores: {lista}.")

    st.markdown("#### 4) ¿Existe relación entre popularidad y calificación?")
    rhos = u.correlaciones_por_tipo(df)
    if rhos:
        for tipo, rho in rhos.items():
            st.write(f"{'Películas' if tipo == 'Movie' else 'Series'}: Spearman = **{u.d(rho, 2)}** → relación **{u.interpretar_rho(rho)}**.")
        st.caption("Asociación, no causalidad. Se calcula por tipo porque las escalas de popularidad difieren.")
    else:
        st.write("No hay suficientes títulos con ≥10 votos bajo estos filtros.")
