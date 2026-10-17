"""
StreamView Analytics - EA2
Portada del dashboard corporativo (Streamlit multipágina).

Ejecutar desde la raíz del proyecto:  streamlit run dashboard/app.py
Páginas:  1_Ejecutivo.py (Directorio y Gerencia General)
          2_Analitico.py (Gerencia de Contenidos y Adquisición)
"""

import sys

import streamlit as st

sys.path.append(".")
from dashboard import utils as u  # noqa: E402

st.set_page_config(page_title="StreamView Analytics", page_icon="🎬", layout="wide")

catalogo, financiero = u.cargar_datos()

st.title("🎬 StreamView Analytics")
st.subheader("Visual Analytics para decisiones estratégicas sobre el catálogo audiovisual")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Títulos en el catálogo", u.n(len(catalogo)))
c2.metric("Películas / Series", f"{u.n((catalogo['type'] == 'Movie').sum())} / {u.n((catalogo['type'] == 'TV Show').sum())}")
c3.metric("Estrenos", f"{catalogo['release_year'].min()}–{catalogo['release_year'].max()}")
c4.metric("Películas con datos financieros", u.n(len(financiero)))

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📊 Dashboard Ejecutivo")
    st.write(
        "**Audiencia:** Directorio y Gerencia General.  \n"
        "**Para qué:** entender rápido el estado del catálogo y apoyar decisiones de "
        "inversión y crecimiento: evolución, géneros, países e idiomas predominantes."
    )
    st.page_link("pages/1_Ejecutivo.py", label="Abrir dashboard ejecutivo", icon="➡️")
with col2:
    st.markdown("### 🔎 Dashboard Analítico")
    st.write(
        "**Audiencia:** Gerencia de Contenidos y Adquisición.  \n"
        "**Para qué:** decidir qué géneros priorizar, qué países son oportunidad y qué "
        "películas rinden con presupuestos reducidos; incluye análisis financiero."
    )
    st.page_link("pages/2_Analitico.py", label="Abrir dashboard analítico", icon="➡️")

st.divider()
with st.expander("Cómo leer estos dashboards (reglas de negocio del caso)", expanded=True):
    st.markdown(
        """
- **Popularidad** es un índice relativo (TMDB); **no** son reproducciones.
- **Calificación** va de 0 a 10 y se promedia solo sobre títulos con **10 o más votos**
  (con menos votos la nota es ruido; un 0 con cero votos significa «sin evaluaciones», no «nota 0»).
- **Presupuesto e ingresos** existen solo para películas, y el análisis financiero
  incluye únicamente películas con **ambos** datos informados.
- **ROI aproximado** = ingresos / presupuesto.
- Cada gráfico indica el período y alcance vigentes según los filtros de la barra lateral.
- Los resultados describen asociaciones, **no causalidad**.
"""
    )
