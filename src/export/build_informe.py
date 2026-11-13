"""
StreamView Analytics - EA3
Genera el informe ejecutivo y el resumen ejecutivo en PDF.
Ejecutar desde la raíz:  python src/export/build_informe.py
Las cifras se calculan desde data/processed/; las imágenes salen de images/.
"""
import sys
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
                                CondPageBreak, Paragraph, Spacer, Table, TableStyle)
from PIL import Image as PILImage

sys.path.append(".")
from src.common import explotar, separar  # noqa: E402

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DV-I", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-B")

AZUL, NARANJA, GRIS, OSC = colors.HexColor("#2563EB"), colors.HexColor("#F97316"), colors.HexColor("#6B7280"), colors.HexColor("#0F172A")
S = {
    "p": ParagraphStyle("p", fontName="DV", fontSize=9.2, leading=13.5, spaceAfter=5),
    "h1": ParagraphStyle("h1", fontName="DV-B", fontSize=15, leading=19, textColor=AZUL, spaceBefore=6, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=10.5, leading=14, textColor=OSC, spaceBefore=6, spaceAfter=3),
    "b": ParagraphStyle("b", fontName="DV", fontSize=9.2, leading=13, leftIndent=12, bulletIndent=2, spaceAfter=2),
    "cap": ParagraphStyle("cap", fontName="DV-I", fontSize=7.8, leading=10, textColor=GRIS, spaceAfter=7, alignment=TA_CENTER),
    "td": ParagraphStyle("td", fontName="DV", fontSize=7.9, leading=10.2),
    "th": ParagraphStyle("th", fontName="DV-B", fontSize=7.9, leading=10.2, textColor=colors.white),
    "tit": ParagraphStyle("tit", fontName="DV-B", fontSize=26, leading=32, textColor=colors.white),
    "sub": ParagraphStyle("sub", fontName="DV", fontSize=12, leading=17, textColor=colors.HexColor("#DBEAFE")),
    "kpi": ParagraphStyle("kpi", fontName="DV-B", fontSize=17, leading=20, textColor=AZUL, alignment=TA_CENTER),
    "kpil": ParagraphStyle("kpil", fontName="DV", fontSize=7.5, leading=9.5, textColor=GRIS, alignment=TA_CENTER),
}
W = A4[0] - 4 * cm


def P(t, s="p"): return Paragraph(t, S[s])
def B(items): return [Paragraph(t, S["b"], bulletText="•") for t in items]


def img(path, width=W, cap=None):
    w, h = PILImage.open(path).size
    out = [Image(path, width=width, height=width * h / w)]
    if cap: out.append(P(cap, "cap"))
    return KeepTogether(out)


def tabla(filas, anchos, cabecera=True):
    data = [[Paragraph(str(c), S["th"] if (i == 0 and cabecera) else S["td"]) for c in f] for i, f in enumerate(filas)]
    t = Table(data, colWidths=anchos, repeatRows=1 if cabecera else 0)
    est = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if cabecera:
        est += [("BACKGROUND", (0, 0), (-1, 0), AZUL)] + [("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F1F5F9")) for i in range(2, len(filas), 2)]
    t.setStyle(TableStyle(est))
    return [t, Spacer(1, 7)]


def pie(c, doc):
    c.saveState(); c.setFont("DV", 7.5); c.setFillColor(GRIS)
    c.drawString(2 * cm, 1.1 * cm, "StreamView Analytics · ADY1104 Visualización de datos · EA3")
    c.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"{doc.page}"); c.restoreState()


def portada(c, doc):
    c.saveState(); c.setFillColor(OSC); c.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    c.setFillColor(NARANJA); c.rect(2 * cm, A4[1] - 3.2 * cm, 2.2 * cm, 0.25 * cm, fill=1, stroke=0); c.restoreState()


def construir(nombre, historia, portada_t, portada_s, primera=portada):
    doc = BaseDocTemplate(nombre, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                          title=portada_t, author="Equipo StreamView Analytics")
    fr = Frame(2 * cm, 2 * cm, W, A4[1] - 4 * cm, id="n")
    doc.addPageTemplates([PageTemplate(id="portada", frames=[Frame(2 * cm, 2 * cm, W, A4[1] - 4 * cm)], onPage=primera),
                          PageTemplate(id="cuerpo", frames=[fr], onPage=pie)])
    from reportlab.platypus import NextPageTemplate
    doc.build([Spacer(1, 7 * cm), P(portada_t, "tit"), Spacer(1, 10), P(portada_s, "sub"), NextPageTemplate("cuerpo"), PageBreak()] + historia)


# ----------------------------------------------------------------- datos ----
cat = pd.read_csv("data/processed/catalogo_limpio.csv")
fin = pd.read_csv("data/processed/catalogo_financiero.csv")
real = fin[fin["presupuesto_realista"]]
n_tit, n_fin = len(cat), len(fin)
cal_m, cal_s = cat.loc[cat.type == "Movie", "calificacion"].mean(), cat.loc[cat.type == "TV Show", "calificacion"].mean()
sp = {t: g["popularity"].corr(g["calificacion"], method="spearman") for t, g in cat.dropna(subset=["calificacion"]).groupby("type")}
roi_ag, roi_med, roi_prom = fin.revenue.sum() / fin.budget.sum(), fin.roi.median(), real.roi.mean()
no_rec = (fin.roi < 1).mean() * 100
q1 = real.budget.quantile(0.25)
n_bajo = int(((real.budget <= q1) & (real.roi >= 3)).sum())
f = lambda x, d=1: f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
n = lambda x: f"{int(x):,}".replace(",", ".")
IM = "images/eda/"; DB = "images/dashboard/"

# ----------------------------------------------------------- INFORME ----
H = []
H += [P("Contenido", "h1")] + [P(t) for t in [
    "1. Descripción del problema de negocio · 2. Objetivos del proyecto · 3. Audiencia objetivo y propósito comunicacional · "
    "4. Fuentes de datos · 5. Análisis exploratorio mediante visualizaciones · 6. Justificación de las representaciones gráficas · "
    "7. Narrativa visual (Data Storytelling) · 8. Diseño e implementación del dashboard interactivo · 9. Evaluación crítica · "
    "10. Conclusiones y recomendaciones · Anexo: reproducción del proyecto"]]
H += [Spacer(1, 6), P("Resumen", "h2"), P(
    f"StreamView administra un catálogo de {n(n_tit)} títulos con reportes dispersos y criterios distintos por área. Este proyecto unifica la información en "
    "dashboards interactivos para el Directorio y la Gerencia de Contenidos, y entrega evidencia para decidir adquisiciones. "
    f"Hallazgos principales: la popularidad es una señal débil de calidad (Spearman {f(sp['Movie'], 2)} en películas y {f(sp['TV Show'], 2)} en series); "
    f"las series están mejor evaluadas ({f(cal_s, 2)}) que las películas ({f(cal_m, 2)}); y financieramente la película mediana rinde {f(roi_med, 1)}x, "
    f"con ≈{f(no_rec, 0)}% que no recupera su presupuesto. La evaluación crítica detectó brechas de confiabilidad, coherencia y narrativa, que se corrigieron en esta etapa.")]

H += [P("1. Descripción del problema de negocio", "h1"),
      P("StreamView Analytics es una plataforma de streaming por suscripción, fundada en 2018, que distribuye películas, series y producciones originales en Latinoamérica. "
        "Cada área usa reportes independientes con criterios distintos, lo que genera múltiples versiones de un mismo indicador, ejecutivos que dedican su tiempo a interpretar reportes, "
        "decisiones de adquisición con información parcial e imposibilidad de comparar con rapidez géneros, países y desempeño financiero.")]
H += [P("<b>Pregunta rectora:</b> ¿qué caracteriza al catálogo, qué contenido genera más interés y valoración, y qué evidencia financiera respalda las decisiones de adquisición de nuevas películas? "
        "Es un problema descriptivo y de comunicación visual (Visual Analytics), no predictivo.")]

H += [P("2. Objetivos del proyecto", "h1"), P("<b>Objetivo general.</b> Transformar los datos del catálogo en conocimiento visual, confiable y accionable que apoye decisiones de inversión y adquisición de contenido."),
      P("<b>Objetivos específicos</b>")] + B([
    "Caracterizar el catálogo por tipo, género, país, idioma y período (EDA).",
    "Medir qué contenido genera más popularidad y mejor calificación, y si ambas se relacionan.",
    "Evaluar la evidencia financiera (presupuesto, ingresos, ROI) disponible para películas.",
    "Entregar dos dashboards interactivos con KPIs y filtros, uno por audiencia, más una vista de calidad de datos.",
    "Evaluar críticamente la solución y aplicar mejoras verificables.",
    "Dejar el proyecto reproducible y documentado."])

H += [P("3. Audiencia objetivo y propósito comunicacional", "h1")]
H += tabla([["Audiencia", "Decisión que apoya", "Propósito comunicacional", "Vista"],
            ["Directorio y Gerencia General", "Dónde invertir y cómo crece el catálogo", "<b>Informar</b> el estado en segundos: KPIs, lectura rápida y pocos filtros", "Dashboard Ejecutivo"],
            ["Gerencia de Contenidos y Adquisición", "Qué géneros, países y películas priorizar", "<b>Explorar y persuadir</b> con evidencia: relaciones, rankings y finanzas", "Dashboard Analítico"],
            ["Data & Analytics", "Qué tan confiable es cada indicador", "<b>Auditar</b>: faltantes, distribuciones, anomalías", "Calidad y EDA"]],
           [3.4 * cm, 4 * cm, 6.2 * cm, 3.4 * cm])
H += [P("Marketing y Producto son audiencias secundarias: usan el dashboard analítico para segmentar por género, país e idioma.")]

H += [P("4. Descripción de las fuentes de datos", "h1")]
H += tabla([["Fuente", "Contenido", "Observaciones"],
            ["netflix_movies_detailed_up_to_2025.csv", "16.000 películas, 18 variables (incluye presupuesto e ingresos)", "Fuente oficial del caso; no se modifica"],
            ["netflix_tv_shows_detailed_up_to_2025.csv", "16.000 series, 16 variables", "Sin datos financieros"],
            ["catalogo_limpio.csv (derivado)", f"{n(n_tit)} títulos unificados con clave única uid", "show_id se repite entre películas y series (397 casos)"],
            ["catalogo_financiero.csv (derivado)", f"{n(n_fin)} películas con presupuesto e ingresos", "22% de las películas; ROI = ingresos / presupuesto"]],
           [5.6 * cm, 6.2 * cm, 5.2 * cm])
H += [P("<b>Calidad y decisiones de limpieza</b> (20 documentadas en <i>reports/data_quality/cleaning_summary.csv</i>):")] + B([
    "Un 0 en votos, presupuesto o ingresos significa «dato no disponible», no «cero».",
    "La calificación solo se considera con 10 o más votos: el 36% de los títulos queda sin calificación válida.",
    "Se eliminaron <i>rating</i> (idéntico a vote_average en 100% de los casos) y <i>duration</i> (100% nula): no existe clasificación etaria.",
    "Presupuestos inferiores a USD 10.000 se excluyen de los rankings de ROI (producen ROI de millones de veces).",
    "La popularidad se compara por percentil dentro de cada tipo, porque series y películas usan escalas distintas.",
    "Limitación del extracto: ≈2.000 títulos por año (≈1.000 películas y ≈1.000 series), por lo que la serie temporal es plana.",
    "<b>Alcance de los datos:</b> las fuentes son de <b>catálogo</b> (contenidos, popularidad, calificación, presupuesto, ingresos). No incluyen usuarios, reproducciones, suscripciones ni dispositivos; por lo tanto este análisis <b>no puede responder retención ni engagement</b> y no debe presentarse como si lo hiciera."])

H += [P("5. Análisis exploratorio mediante visualizaciones", "h1"),
      P("El EDA siguió la estrategia analítica de la guía 3.1.1: comprender el problema, revisar variables y calidad, analizar cada variable, explorar relaciones, identificar patrones y formular hipótesis.")]
H += [P("5.1 Estructura del catálogo", "h2"), img(IM + "01_distribucion_tipo.png", 6 * cm, "Figura 1. Película vs. serie: catálogo equilibrado (50,0% / 50,0%)."),
      img(IM + "02_generos_predominantes.png", W * 0.82, "Figura 2. Géneros predominantes: Drama (14.773), Comedy (9.106) y Animation (4.070)."),
      img(IM + "03_paises.png", W * 0.82, "Figura 3. Países: Estados Unidos (10.955), Japón (2.869) y Reino Unido (2.608); 147 países en total."),
      img(IM + "04_idiomas.png", W * 0.82, "Figura 4. Idiomas: 83 en total; el inglés concentra la mayoría.")]
H += [P("5.2 Popularidad y calificación", "h2"),
      P(f"La calificación promedio es <b>{f(cat.calificacion.mean(), 2)}</b> sobre los {n(cat.calificacion.notna().sum())} títulos con 10 o más votos: películas {f(cal_m, 2)} y series {f(cal_s, 2)}. "
        f"La relación entre popularidad y calificación es débil: Spearman {f(sp['Movie'], 2)} en películas y {f(sp['TV Show'], 2)} en series."),
      img(IM + "05_comparativa_popularidad.png", 7 * cm, "Figura 5. Popularidad normalizada por tipo (boxplot, sin valores extremos)."),
      img(IM + "06_popularidad_vs_calificacion.png", W * 0.7, "Figura 6. Dispersión popularidad (escala log) vs. calificación: nube difusa, sin patrón fuerte."),
      img(IM + "11_distribucion_calificacion.png", W * 0.78, "Figura 7. Distribución de la calificación por tipo."),
      img(IM + "10_correlaciones.png", W * 0.62, "Figura 8. Matriz de correlaciones entre variables numéricas.")]
H += [P("5.3 Evolución temporal", "h2"), img(IM + "07_evolucion_historica.png", W * 0.78, "Figura 9. Estrenos por año: serie plana (≈1.000 películas y ≈1.000 series por año)."),
      P("<b>Advertencia:</b> la ausencia de tendencia es una característica del extracto entregado, no un hallazgo de negocio.")]
H += [P("5.4 Análisis financiero", "h2"),
      P(f"Solo {n(n_fin)} títulos ({f(n_fin / n_tit * 100, 0)}% del catálogo; 22% de las películas) tienen presupuesto e ingresos. Presupuesto promedio USD {f(fin.budget.mean() / 1e6, 1)} millones; "
        f"ingresos acumulados USD {n(fin.revenue.sum() / 1e6)} millones. Se usan tres definiciones de ROI y no deben mezclarse:")]
H += tabla([["Definición de ROI", "Valor", "Uso"],
            ["Agregado (ingresos totales / presupuesto total)", f"{f(roi_ag, 1)}x", "KPI de los dashboards y Power BI"],
            ["Mediano por película", f"{f(roi_med, 1)}x", "Referencia de riesgo: la película típica"],
            ["Promedio por película (presupuesto ≥ USD 10.000)", f"{f(roi_prom, 1)}x", "Inflado por pocos éxitos de bajo costo"],
            ["Promedio sin filtrar", f"{f(fin.roi.mean(), 0)}x", "Distorsionado por presupuestos cercanos a USD 1; no usar"]],
           [8 * cm, 2.4 * cm, 6.6 * cm])
H += [img(IM + "08_presupuesto_vs_ingresos.png", W * 0.7, "Figura 10. Presupuesto vs. ingresos (log-log): bajo la línea roja la película pierde dinero."),
      img(IM + "09_top_roi.png", W * 0.75, "Figura 11. Top 15 por ROI (presupuesto ≥ USD 10.000)."),
      P("5.5 Hipótesis surgidas", "h2")] + B([
    "H1. La popularidad no es sustituto de la calidad.",
    "H2. Asia (Japón y Corea del Sur) combina volumen y buena calificación; México y Colombia rinden en popularidad con poco volumen.",
    "H3. Las películas de bajo presupuesto con ROI atípico son oportunidades si el dato se valida (puede ser error de carga)."])

H += [P("6. Justificación de las representaciones gráficas", "h1"),
      P("Cada gráfico se eligió según el tipo de variable y la pregunta que responde (patrones analíticos de la guía 3.1.1). Paleta única: azul = película, naranja = serie; sin 3D ni adornos.")]
H += tabla([["Pregunta (patrón)", "Gráfico elegido", "Por qué", "Alternativa descartada"],
            ["Composición del catálogo (comparación)", "Barra simple / barras horizontales", "Longitud es la codificación más precisa; nombres largos legibles", "Torta con 83 idiomas: ilegible"],
            ["Distribución de una variable", "Histograma y boxplot por tipo", "Muestra forma, dispersión y extremos; compara dos grupos", "Solo promedios: ocultan la dispersión"],
            ["Relación popularidad-calificación (relación)", "Dispersión, eje log, + Spearman por tipo", "Dos numéricas; asimetría fuerte; escalas distintas por tipo", "Pearson global: distorsionado"],
            ["Presupuesto vs. ingresos (relación)", "Dispersión log-log con línea ROI = 1", "Rango de varios órdenes de magnitud; la línea separa ganancia de pérdida", "Ejes lineales: puntos aplastados"],
            ["Dónde se produce (concentración)", "Mapa coroplético + barras Top 10", "El mapa muestra el patrón; la barra, la posición exacta", "Solo mapa: no permite leer cifras"],
            ["Peso de cada género (part-to-whole)", "Treemap (color = calificación)", "El área expresa participación y suma una segunda variable", "Torta con 27 géneros"],
            ["Evolución (tendencia)", "Áreas / líneas", "Variable temporal continua; superpone estreno e incorporación", "Barras: fragmentan la serie"],
            ["Valores atípicos (anomalías)", "Strip plot con regla IQR sobre log(ROI)", "Resalta puntos inusuales sin esconderlos", "Eliminarlos sin revisar"]],
           [3.9 * cm, 3.7 * cm, 5.4 * cm, 4 * cm])

H += [P("6.1 Atributos visuales y criterios de representación", "h2")]
H += tabla([["Atributo visual", "Decisión", "Justificación analítica y de comunicación"],
            ["Posición y longitud (barras)", "Rankings y comparaciones con barras ordenadas", "Son los canales que el ojo decodifica con más precisión; permiten leer diferencias pequeñas entre categorías"],
            ["Color", "Azul = película / valor principal; naranja = serie / segunda serie; secuencial azul para magnitud", "Un color con significado constante evita releer la leyenda; azul-naranja se distingue en daltonismo; sin rojo-verde"],
            ["Tamaño (puntos)", "Votos en la dispersión popularidad-calificación", "Indica cuánta evidencia respalda cada punto sin agregar un gráfico más"],
            ["Escala logarítmica", "Popularidad, votos, presupuesto e ingresos", "Distribuciones muy asimétricas: en escala lineal casi todos los puntos quedarían aplastados"],
            ["Eje desde cero", "Barras, áreas y evolución temporal", "Un eje truncado exagera diferencias (el caso de 2025: 9 títulos parecían una caída fuerte)"],
            ["Etiquetas y alcance", "Valores sobre las barras y período/filtros bajo cada título", "El lector sabe qué está mirando sin depender de memoria ni de tooltips"],
            ["Jerarquía visual", "KPIs arriba, conclusión (Lectura rápida), luego gráficos", "El directivo lee primero la conclusión y baja al detalle solo si lo necesita"]],
           [3.6 * cm, 5.4 * cm, 8 * cm])

H += [P("7. Desarrollo de la narrativa visual (Data Storytelling)", "h1"),
      P("La narrativa sigue un arco de cinco escenas: contexto, hallazgo, tensión, evidencia y llamado a la acción. El dashboard ejecutivo adelanta la conclusión («Lectura rápida») y el analítico entrega el detalle para quien quiera profundizar.")]
H += tabla([["Escena", "Mensaje", "Visual", "Dónde"],
            ["1. Contexto", "Cada área mide distinto; hay un catálogo grande y desordenado", "KPIs de estado del catálogo", "Ejecutivo"],
            ["2. Hallazgo", f"Catálogo equilibrado ({n(16000)} / {n(15991)}), dominado por Drama y EE. UU.", "Barras Top 10, mapa", "Ejecutivo"],
            ["3. Tensión", "Lo más popular no es lo mejor evaluado", "Dispersión + Spearman por tipo", "Analítico"],
            ["4. Evidencia", f"Series mejor evaluadas; Asia sobresale; ROI mediano {f(roi_med, 1)}x y ≈{f(no_rec, 0)}% no recupera inversión", "Barras por género/país, dispersión financiera", "Analítico"],
            ["5. Acción", f"Priorizar Asia y pilotos en México/Colombia; validar los {n_bajo} casos de bajo presupuesto con ROI ≥ 3", "Tabla «éxitos con presupuesto reducido», Conclusiones", "Analítico"],
            ["Confianza", "Qué tan confiable es cada número", "Faltantes, distribuciones, anomalías", "Calidad y EDA"]],
           [2.5 * cm, 6.5 * cm, 5 * cm, 3 * cm])
H += [P("Recursos narrativos aplicados: título y alcance visibles en cada vista, color con significado constante, anotaciones de limitaciones donde el dato engaña (serie plana, ROI atípico) y conclusiones calculadas que cambian con los filtros.")]

H += [P("8. Diseño e implementación del dashboard interactivo", "h1"),
      P("<b>Arquitectura.</b> Datos crudos → <i>src/data/clean_data.py</i> (limpieza y reglas de negocio) → <i>data/processed/</i> → dashboards. Tecnologías: Streamlit y Plotly (dashboard principal), Dash (vista financiera), D3 (treemap), Matplotlib/Seaborn (EDA) y un modelo en estrella con medidas DAX para Power BI (el archivo .pbix se construye con la guía incluida).")]
H += tabla([["Componente", "Contenido"],
            ["KPIs", "Títulos, películas, series, países, idiomas, géneros, popularidad y calificación promedio; KPIs financieros (presupuesto, ingresos, ROI) en el analítico"],
            ["Filtros", "Tipo, rango de años, género; en el analítico además país, idioma y rango de calificación. Todos actualizan KPIs y gráficos; el alcance se muestra bajo el título"],
            ["Interacción", "Tooltips, zoom, pestañas por tema, umbrales ajustables (votos mínimos, percentil de presupuesto, ROI) y descarga de lo filtrado en CSV"],
            ["Reglas de negocio visibles", "Qué es popularidad, cómo se calcula la calificación, qué es ROI y por qué no hay causalidad"]],
           [3.2 * cm, 13.8 * cm])
H += [img(DB + "01_ejecutivo.png", W * 0.95, "Figura 12. Dashboard Ejecutivo con la «Lectura rápida» agregada en EA3."),
      img(DB + "02_analitico.png", W * 0.95, "Figura 13. Dashboard Analítico (Contenidos y Adquisición)."),
      img(DB + "03_calidad_eda.png", W * 0.95, "Figura 14. Nueva página «Calidad y EDA» (EA3).")]

H += [CondPageBreak(7 * cm), P("9. Evaluación crítica de la solución", "h1"),
      P("La evaluación se hizo contra cuatro preguntas: ¿qué funciona y con qué evidencia?, ¿qué decisiones de diseño se tomaron y por qué?, ¿qué limitaciones, sesgos y riesgos tiene y cómo se mitigan?, y ¿qué mejorar primero? Los detalles de trabajo están en <i>docs/evaluacion_critica.md</i>."),
      P("9.1 Fortalezas, con evidencia", "h2")]
H += tabla([["Fortaleza", "Evidencia verificable", "Por qué importa para decidir"],
            ["Audiencia y decisión explícitas por vista", "Tres vistas con audiencia y propósito declarados en la portada del dashboard", "Cada área ve solo lo que necesita para su decisión"],
            ["Reglas de negocio visibles", "Nota solo con ≥ 10 votos, 0 = «sin dato» y definición de ROI en la portada y en los tooltips", "El mismo indicador significa lo mismo para todos"],
            ["Limpieza trazable", "20 decisiones documentadas en reports/data_quality/cleaning_summary.csv", "Los números se pueden auditar"],
            ["Interacción útil", "3 filtros en el ejecutivo y 6 en el analítico; alcance visible; umbrales ajustables; exportación CSV", "El usuario explora sin pedir un reporte nuevo"],
            ["Autocrítica verificable", "6 mejoras con antes→después (docs/mejoras_ea3.md) y página de calidad de datos", "La solución revela cuánta confianza merece cada cifra"],
            ["Reproducibilidad", "El proyecto se ejecutó desde una copia limpia sin errores; datos procesados incluidos", "Otro equipo puede repetir y verificar el análisis"]],
           [3.6 * cm, 7.4 * cm, 6 * cm])
H += [P("9.2 Principales decisiones de diseño y su justificación", "h2")]
H += tabla([["Decisión", "Alternativa considerada", "Justificación"],
            ["Streamlit + Plotly como dashboard principal", "Power BI", "Comparte el mismo pipeline de limpieza en Python, filtros nativos y un solo código para dashboard, EDA y notebook; el modelo para Power BI se dejó listo"],
            ["Dos dashboards por audiencia", "Un solo tablero para todos", "El Directorio necesita estado y conclusión; Contenidos necesita explorar. Mezclarlos satura a ambos"],
            ["Spearman por tipo", "Pearson global", "Las variables son muy asimétricas y películas y series tienen escalas de popularidad distintas"],
            ["Popularidad como percentil dentro del tipo", "Popularidad cruda", "Permite comparar géneros y países sin mezclar escalas"],
            ["Calificación solo con ≥ 10 votos", "Usar todos los títulos", "Con menos votos la nota es ruido; incluir ceros bajaba el promedio de 6,63 a 5,69"]],
           [4.2 * cm, 3.6 * cm, 9.2 * cm])
H += [P("9.3 Limitaciones, sesgos y riesgos, con medidas de mitigación", "h2")]
H += tabla([["Tipo", "Descripción y evidencia", "Riesgo para la decisión", "Mitigación"],
            ["Limitación de alcance", "Solo datos de catálogo: sin usuarios, reproducciones, suscripciones ni dispositivos", "Responder retención o engagement con datos que no lo sustentan", "Declarar el alcance en cada vista; solicitar esas tablas (prioridad 1); no inferir comportamiento desde la popularidad"],
            ["Sesgo de cobertura financiera", "Solo el 22% de las películas tiene datos financieros, y son las más conocidas: mediana de 1.007 votos vs. 101 y popularidad relativa de 0,70 vs. 0,44", "Creer que el ROI describe todo el catálogo cuando describe películas grandes", "Rotular «solo películas con datos financieros»; usar ROI mediano; solicitar mayor cobertura"],
            ["Sesgo de selección en la calificación", "Solo 64% de los títulos tiene ≥ 10 votos y esos son más populares (mediana de popularidad 11,1 vs. 9,4 en películas; 40,6 vs. 33,6 en series)", "La nota refleja títulos conocidos, no el catálogo completo", "Umbral visible y ajustable; mostrar el % con calificación válida en la página de calidad"],
            ["Sesgo de origen", "El inglés es el 43,7% de los títulos y Estados Unidos el 34,2%", "Rankings dominados por volumen, no por rendimiento", "Mínimo de títulos por país; comparar nota y percentil de popularidad, no solo cantidad"],
            ["Sesgo de composición", "Japón y Corea del Sur tienen 60% a 65% de series, que puntúan más (7,29 vs. 6,35); la nota agregada por país mezcla tipos y su cobertura de nota va de 53% a 90%", "Atribuir al país lo que es efecto del tipo de contenido", "Comparar siempre dentro de cada tipo y mostrar la cantidad de títulos con nota"],
            ["Sesgo de muestreo temporal", "≈1.000 películas y ≈1.000 series por año: serie construida, no crecimiento real", "Leer una tendencia inexistente", "Advertencia en pantalla y eje desde cero; no interpretar tendencias"],
            ["Riesgo de datos atípicos", "ROI promedio sin filtrar de 781x por presupuestos cercanos a USD 1", "Invertir basándose en un error de carga", "Filtro de presupuesto ≥ USD 10.000, pestaña de anomalías y validación en la fuente"],
            ["Riesgo de interpretación", "Correlaciones débiles (Spearman 0,17 a 0,23)", "Tomar asociación por causalidad o popularidad por calidad", "Advertencias «correlación ≠ causalidad»; decisión final humana"]],
           [2.7 * cm, 5.1 * cm, 4.2 * cm, 5 * cm])
H += [P("9.4 Mejoras implementadas en esta etapa (antes → después)", "h2")]
H += tabla([["ID", "Limitación detectada (antes)", "Mejora implementada (después)"],
            ["M1", "No se veía cuán confiables eran los resultados", "Página «Calidad y EDA»: faltantes, distribuciones, correlaciones y anomalías"],
            ["M2", "Cifras del EDA distintas a las de los dashboards (nota 5,69 vs. 6,63; Pearson 0,03; «crecimiento sostenido»)", "Criterio único en todo el proyecto; Spearman por tipo; tres definiciones de ROI documentadas"],
            ["M3", "La conclusión quedaba a cargo del lector", "«Lectura rápida» dinámica en el dashboard ejecutivo"],
            ["M4", "No se podía llevar lo filtrado a otras herramientas", "Descarga en CSV de los títulos filtrados"],
            ["M5", "Datos procesados ignorados, sin notebook, README solo para Windows", "Datos incluidos, notebook .ipynb y README multiplataforma"],
            ["M6", "El eje truncado de la evolución temporal exageraba una caída de 9 títulos", "Eje Y desde cero"]],
           [1.2 * cm, 7.4 * cm, 8.4 * cm])
H += [P("9.5 Oportunidades de mejora, priorizadas", "h2"),
      P("Criterio: impacto sobre la decisión dividido por el esfuerzo. La clasificación es un juicio del equipo, no una medición. Las mejoras ya implementadas (M1 a M6) están en la sección 9.4 y en <i>docs/mejoras_ea3.md</i>.")]
H += tabla([["Prio.", "Mejora", "Impacto", "Esfuerzo", "Viabilidad y fundamento"],
            ["1", "Solicitar tablas de usuarios, reproducciones y suscripciones, más clasificación etaria y cobertura financiera", "Alto", "Medio (depende del proveedor)", "Viable como requerimiento formal; habilita analizar retención y engagement, hoy imposibles"],
            ["2", "Pruebas automatizadas de limpieza y KPI", "Alto", "Bajo", "Evita repetir el problema de cifras distintas entre documentos (mejora M2)"],
            ["3", "Prueba de usabilidad con 3 a 5 usuarios de Directorio y Contenidos", "Alto", "Bajo", "Comprueba que la Lectura rápida y los filtros se entienden; no hay evidencia de uso real todavía"],
            ["4", "Desplegar el dashboard en la web", "Medio", "Bajo", "Acceso sin instalar Python; el código ya corre con Streamlit"],
            ["5", "Revisión de accesibilidad (contraste, lector de pantalla)", "Medio", "Bajo", "La paleta ya considera daltonismo; falta verificar el resto"],
            ["6", "Construir el archivo .pbix", "Medio", "Medio", "Sirve a usuarios sin Python; el modelo y las medidas DAX ya existen"]],
           [1.1 * cm, 6 * cm, 1.8 * cm, 2.9 * cm, 5.2 * cm])

H += [CondPageBreak(7 * cm), P("10. Conclusiones y recomendaciones para la toma de decisiones", "h1"), P("10.1 Conclusiones", "h2")] + B([
    f"El catálogo está equilibrado entre películas y series, pero concentrado en Drama y Estados Unidos.",
    f"La popularidad es una señal débil de calidad (Spearman {f(sp['Movie'], 2)} y {f(sp['TV Show'], 2)}): decidir solo por ella es riesgoso.",
    f"Las series están mejor evaluadas ({f(cal_s, 2)}) que las películas ({f(cal_m, 2)}), pero solo el 38% de las series tiene 10 o más votos: es una comparación con sesgo de selección.",
    f"Financieramente, la película típica rinde {f(roi_med, 1)}x y ≈{f(no_rec, 0)}% no recupera su presupuesto; el promedio engaña.",
    "La evaluación crítica mejoró la confiabilidad, la coherencia y la narrativa; las limitaciones restantes son del dato, no del diseño."])
H += [P("10.2 Recomendaciones", "h2")]
H += tabla([["#", "Recomendación", "Evidencia", "Cautela"],
            ["R1", "No usar la popularidad como sustituto de la calidad; mirar ambas", f"Spearman {f(sp['Movie'], 2)}–{f(sp['TV Show'], 2)}", "Asociación, no causalidad"],
            ["R2", "Priorizar adquisiciones de Japón y Corea del Sur; pilotos de series de México y Colombia", "Dentro de cada tipo, Japón supera a EE. UU. (películas 6,90 vs. 6,26; series 7,45 vs. 7,21) y Corea del Sur también (6,82 y 7,34); series de México y Colombia con popularidad relativa 0,69 y 0,63 vs. 0,57 de EE. UU.", "Solo 53% (Corea) a 77% (México) de los títulos tiene nota; Colombia: 90 series"],
            ["R3", "Priorizar series Sci-Fi & Fantasy y Action & Adventure; películas de Aventura, Acción y Fantasía", "Series 7,45 y 7,43 de nota; películas con mayor popularidad relativa", "Popularidad es relativa, no reproducciones"],
            ["R4", "Explorar películas de bajo presupuesto con ROI alto, validando antes el dato", f"{n_bajo} películas con presupuesto ≤ USD {f(q1 / 1e6, 0)} M y ROI ≥ 3", "Pueden ser errores de carga"],
            ["R5", "Usar ROI mediano y % que no recupera inversión como referencia de riesgo", f"{f(roi_med, 1)}x y ≈{f(no_rec, 0)}%", "Solo 22% con datos financieros"],
            ["R6", "Mejorar la fuente: clasificación etaria, reproducciones y cobertura financiera", "Limitaciones del extracto", "Depende del proveedor"],
            ["R7", "Adoptar estos dashboards como versión única de cada indicador", "Problema de múltiples versiones", "Requiere gobierno de datos"]],
           [0.9 * cm, 6.2 * cm, 5.3 * cm, 4.6 * cm])
H += [P("Estos resultados apoyan, no reemplazan, el criterio humano en decisiones de adquisición (ver <i>docs/etica_privacidad.md</i>).")]

H += [P("10.3 Impacto esperado en la toma de decisiones", "h2"),
      P("La solución no decide por la organización: cambia <b>qué evidencia ve quien decide</b>. La tabla compara cada decisión sin y con la solución. No se estiman ahorros en cifras porque no se midió una línea base; en su lugar se indica cómo medir el impacto.")]
H += tabla([["Decisión", "Sin la solución", "Con la solución (evidencia)", "Cómo se mediría"],
            ["Qué contenido adquirir", "Se usa la popularidad como sustituto de la calidad", f"Se muestra que la relación es débil (Spearman {f(sp['Movie'], 2)} y {f(sp['TV Show'], 2)}); se exige mirar ambas", "% de adquisiciones evaluadas con popularidad y calificación"],
            ["En qué mercados buscar", "El volumen domina (EE. UU.: 34% de los títulos)", "Se identifican mercados con mejor nota dentro de cada tipo (Japón y Corea del Sur sobre EE. UU.) y series con popularidad relativa alta (México, Colombia)", "Pilotos realizados por mercado y su nota posterior"],
            ["Cuánto riesgo financiero asumir", f"Cifras de ROI contradictorias entre reportes (781x, {f(roi_prom, 1)}x, {f(roi_ag, 1)}x)", f"Referencia única: mediana {f(roi_med, 1)}x y ≈{f(no_rec, 0)}% de películas que no recupera su presupuesto", "Adopción del ROI mediano en el comité de adquisición"],
            ["Cuándo confiar en un dato", "Cada área usa criterios distintos", "Una definición por indicador, reglas visibles y página de calidad de datos", "Cantidad de definiciones distintas por indicador (meta: una)"],
            ["Rapidez de lectura directiva", "Se interpretan reportes largos", "KPIs y «Lectura rápida» con la conclusión primero", "Tiempo de lectura medido en la prueba de usabilidad (línea base por levantar)"]],
           [3 * cm, 3.9 * cm, 5.9 * cm, 4.2 * cm])

H += [P("Anexo. Reproducción del proyecto", "h1"),
      P("<font face='DV'>pip install -r requirements.txt<br/>python src/data/clean_data.py<br/>python notebooks/01_analisis_completo.py<br/>streamlit run dashboard/app.py<br/>python src/export/build_informe.py</font>"),
      P("Estructura: data/ (crudos y procesados), src/ (código), notebooks/, dashboard/ (Streamlit), dash_app/, d3/, powerbi/, images/, reports/, docs/ y README.md.")]

construir("docs/Informe_Ejecutivo_StreamView_EA3.pdf", H, "Informe ejecutivo<br/>StreamView Analytics",
          "Visual Analytics del catálogo audiovisual<br/>ADY1104 Visualización de datos · Evaluación EP6 · Duoc UC<br/><br/>Integrantes: [completar]<br/>Docente: [completar] · Noviembre 2026")

# ---------------------------------------------------------- RESUMEN ----
R = [P("Resumen ejecutivo", "h1")]
kp = [[Paragraph(v, S["kpi"]) for v in [n(n_tit), f(cal_s, 2) + " vs " + f(cal_m, 2), f(sp["Movie"], 2), f(roi_med, 1) + "x"]],
      [Paragraph(t, S["kpil"]) for t in ["títulos analizados", "calificación series vs. películas", "Spearman popularidad-calificación (películas)", "ROI mediano por película"]]]
tk = Table(kp, colWidths=[W / 4] * 4); tk.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EFF6FF")), ("BOX", (0, 0), (-1, -1), 0.5, AZUL), ("TOPPADDING", (0, 0), (-1, -1), 5)]))
R += [tk, Spacer(1, 8),
      P("El problema", "h2"), P("StreamView decide adquisiciones con reportes dispersos y criterios distintos por área, sin una versión única de sus indicadores."),
      P("Principales hallazgos", "h2")] + B([
    f"<b>Popularidad no es calidad:</b> la relación es débil (Spearman {f(sp['Movie'], 2)} en películas, {f(sp['TV Show'], 2)} en series).",
    f"<b>Las series se evalúan mejor</b> ({f(cal_s, 2)}) que las películas ({f(cal_m, 2)}), aunque solo el 38% de las series tiene nota válida.",
    "<b>Asia sobresale, comparando dentro de cada tipo:</b> Japón y Corea del Sur superan a EE. UU. en películas y en series; las series de México y Colombia rinden en popularidad con poco volumen.",
    f"<b>Finanzas:</b> la película mediana rinde {f(roi_med, 1)}x y ≈{f(no_rec, 0)}% no recupera su presupuesto; hay {n_bajo} películas de bajo presupuesto con ROI ≥ 3 que conviene validar.",
    "<b>Límites del dato:</b> sin clasificación etaria, serie temporal plana y finanzas solo para el 22% de las películas."])
R += [P("La solución propuesta", "h2"),
      P("Tres vistas interactivas con KPIs, filtros y alcance visible: <b>Ejecutivo</b> (Directorio), <b>Analítico</b> (Contenidos y Adquisición) y <b>Calidad y EDA</b> (confiabilidad de los datos). "
        "Tras la evaluación crítica se agregaron: lectura rápida con la conclusión primero, página de calidad de datos, cifras unificadas y exportación de lo filtrado.")]
R += [P("Recomendaciones", "h2")] + B([
    "Decidir con popularidad <b>y</b> calificación, nunca solo con la primera.",
    "Priorizar adquisiciones de Asia y pilotos en México y Colombia.",
    "Validar en la fuente las películas de bajo presupuesto con ROI alto antes de invertir.",
    "Usar el ROI mediano y el porcentaje que no recupera inversión como referencia de riesgo.",
    "Solicitar al proveedor clasificación etaria, reproducciones reales y más cobertura financiera.",
    "Adoptar estos dashboards como versión única de los indicadores."])
R += [P("Impacto esperado", "h2"),
      P("La solución cambia qué evidencia ve quien decide: deja de usarse la popularidad como sustituto de la calidad, se adopta una referencia única de riesgo financiero (ROI mediano) y cada cifra muestra cuánta confianza merece. "
        "No se estiman ahorros porque no hay línea base; el informe propone cómo medir el impacto.")]
construir("docs/Resumen_Ejecutivo_StreamView_EA3.pdf", R, "Resumen ejecutivo<br/>StreamView Analytics", "Hallazgos, solución y recomendaciones<br/>ADY1104 · EA3 · Duoc UC")
print("ok")
