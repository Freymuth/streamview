// StreamView Analytics - EA6: genera docs/StreamView_Presentacion_EA3.pptx (11 diapositivas, ~10 min)
// Ejecutar desde la raíz: node src/export/build_presentacion.js   (requiere pptxgenjs)
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/mnt/skills/public/pptx/scripts/apply_theme.js");

const THEME = { name: "StreamView", headFontFace: "Calibri", bodyFontFace: "Calibri",
  colors: { dk1: "0F172A", lt1: "FFFFFF", dk2: "1E293B", lt2: "F1F5F9", accent1: "2563EB", accent2: "F97316",
            accent3: "0D9488", accent4: "6B7280", accent5: "93C5FD", accent6: "FDBA74", hlink: "2563EB", folHlink: "6B7280" } };
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "StreamView Analytics - Presentación y defensa";
pres.author = "Equipo StreamView Analytics";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

pres.defineSlideMaster({ title: "PORTADA", background: { color: "0F172A" } });
pres.defineSlideMaster({ title: "CONTENIDO", background: { color: "FFFFFF" },
  objects: [{ rect: { x: 0, y: 0, w: 0.18, h: 5.625, fill: { color: "2563EB" } } }],
  slideNumber: { x: 9.3, y: 5.3, w: 0.5, h: 0.25, fontSize: 9, color: "6B7280" } });

const card = (s, x, y, w, h, color = "F1F5F9") => s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color }, line: { color: "E2E8F0", width: 0.75 } });
const title = (s, t, sub) => {
  s.addText(t, { x: 0.5, y: 0.25, w: 9, h: 0.55, fontSize: 24, bold: true, color: "0F172A", isTextBox: true, margin: 0 });
  if (sub) s.addText(sub, { x: 0.5, y: 0.8, w: 9, h: 0.32, fontSize: 12.5, color: "6B7280", isTextBox: true, margin: 0 });
};
const hdr = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: "2563EB" }, fontSize: 10.5 } });
const cell = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 9.5, color: "1E293B", valign: "top" }, o) });
const stat = (s, x, y, w, num, label, color = "2563EB") => {
  card(s, x, y, w, 1.25);
  s.addText(num, { x, y: y + 0.08, w, h: 0.6, fontSize: 30, bold: true, color, align: "center", isTextBox: true, margin: 0 });
  s.addText(label, { x: x + 0.08, y: y + 0.7, w: w - 0.16, h: 0.5, fontSize: 10, color: "475569", align: "center", isTextBox: true, margin: 0 });
};
const bullets = (items, o) => items.map((t, i) => ({ text: t, options: Object.assign({ bullet: true, breakLine: i < items.length - 1 }, o || {}) }));
const TB = { border: { type: "solid", pt: 0.5, color: "CBD5E1" }, fontFace: "Calibri" };

// 1 PORTADA
let s = pres.addSlide({ masterName: "PORTADA" });
s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.35, w: 0.9, h: 0.09, fill: { color: "F97316" }, line: { color: "F97316", width: 0 } });
s.addText("StreamView Analytics", { x: 0.6, y: 1.55, w: 8.8, h: 0.9, fontSize: 44, bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
s.addText("Visual Analytics del catálogo audiovisual: solución, evaluación crítica y recomendaciones", { x: 0.6, y: 2.5, w: 8.8, h: 0.7, fontSize: 19, color: "BFDBFE", isTextBox: true, margin: 0 });
s.addText("ADY1104 Visualización de datos · Evaluación EP6 · Duoc UC", { x: 0.6, y: 3.4, w: 8.8, h: 0.35, fontSize: 14, color: "94A3B8", isTextBox: true, margin: 0 });
s.addText("Integrantes: [completar]   ·   Docente: [completar]", { x: 0.6, y: 3.8, w: 8.8, h: 0.35, fontSize: 14, color: "94A3B8", isTextBox: true, margin: 0 });
s.addNotes("[0:15] Presentación. Son 10 minutos: problema, datos, EDA, diseño, dashboard, storytelling, evaluación crítica, mejoras, recomendaciones e impacto. Cada integrante debe poder responder sobre cualquier apartado: las preguntas son cruzadas.");

// 2 PROBLEMA
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "1. Problema de negocio", "Cada área mide distinto: no hay una versión única de los indicadores del catálogo");
card(s, 0.5, 1.3, 4.3, 1.45);
s.addText([{ text: "Contexto", options: { bold: true, fontSize: 13, color: "2563EB", breakLine: true } },
  ...bullets(["Plataforma de streaming por suscripción, miles de títulos", "Reportes independientes con criterios distintos", "Decisiones de adquisición con información parcial"])],
  { x: 0.62, y: 1.36, w: 4.1, h: 1.35, fontSize: 11.5, color: "1E293B", valign: "top", isTextBox: true, margin: 0 });
card(s, 5.0, 1.3, 4.5, 1.45);
s.addText([{ text: "Objetivos de comunicación", options: { bold: true, fontSize: 13, color: "2563EB", breakLine: true } },
  ...bullets(["Informar el estado del catálogo en segundos", "Explorar qué contenido priorizar", "Mostrar cuánta confianza merece cada dato"])],
  { x: 5.12, y: 1.36, w: 4.3, h: 1.35, fontSize: 11.5, color: "1E293B", valign: "top", isTextBox: true, margin: 0 });
s.addTable([[hdr("Audiencia"), hdr("Decisión que apoya"), hdr("Vista")],
  [cell("Directorio y Gerencia General", { bold: true }), cell("Estado del catálogo y dónde invertir"), cell("Dashboard Ejecutivo")],
  [cell("Contenidos y Adquisición", { bold: true }), cell("Qué géneros, países y películas priorizar"), cell("Dashboard Analítico")],
  [cell("Data & Analytics", { bold: true }), cell("Qué tan confiable es cada número"), cell("Calidad y EDA")]],
  Object.assign({ x: 0.5, y: 3.0, w: 9, colW: [3, 3.7, 2.3], rowH: 0.42 }, TB));
s.addNotes("[0:50] Contexto organizacional, audiencia y objetivos de comunicación. Tres audiencias, tres vistas. Pregunta rectora: qué caracteriza al catálogo, qué contenido genera más interés y valoración, y qué evidencia financiera respalda las adquisiciones.");

// 3 FUENTES
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "2. Fuentes de datos e integración", "Dos archivos de catálogo integrados con una clave única");
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.35, w: 2.3, h: 0.7, fill: { color: "DBEAFE" }, line: { color: "2563EB", width: 1 } });
s.addText("16.000 películas\n18 variables", { x: 0.5, y: 1.35, w: 2.3, h: 0.7, fontSize: 11, bold: true, color: "0F172A", align: "center", valign: "middle", isTextBox: true, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.25, w: 2.3, h: 0.7, fill: { color: "FFEDD5" }, line: { color: "F97316", width: 1 } });
s.addText("16.000 series\n16 variables", { x: 0.5, y: 2.25, w: 2.3, h: 0.7, fontSize: 11, bold: true, color: "0F172A", align: "center", valign: "middle", isTextBox: true, margin: 0 });
s.addText("→", { x: 2.85, y: 1.85, w: 0.5, h: 0.5, fontSize: 28, color: "6B7280", align: "center", isTextBox: true, margin: 0 });
card(s, 3.4, 1.35, 2.7, 1.6);
s.addText([{ text: "Limpieza e integración", options: { bold: true, fontSize: 12, color: "2563EB", breakLine: true } },
  ...bullets(["Clave única uid (show_id se repite en 397 casos)", "20 decisiones documentadas", "0 = «sin dato», no cero"])],
  { x: 3.5, y: 1.4, w: 2.5, h: 1.5, fontSize: 10.5, color: "1E293B", valign: "top", isTextBox: true, margin: 0 });
s.addText("→", { x: 6.15, y: 1.85, w: 0.5, h: 0.5, fontSize: 28, color: "6B7280", align: "center", isTextBox: true, margin: 0 });
card(s, 6.7, 1.35, 2.8, 1.6);
s.addText([{ text: "Resultado", options: { bold: true, fontSize: 12, color: "2563EB", breakLine: true } },
  ...bullets(["Catálogo: 31.991 títulos", "Financiero: 3.540 películas (22% de las películas)"])],
  { x: 6.8, y: 1.4, w: 2.6, h: 1.5, fontSize: 10.5, color: "1E293B", valign: "top", isTextBox: true, margin: 0 });
s.addText([{ text: "Variables relevantes: ", options: { bold: true } }, { text: "tipo, género, país, idioma, año, popularidad, calificación (≥ 10 votos), votos, presupuesto, ingresos." }],
  { x: 0.5, y: 3.15, w: 9, h: 0.5, fontSize: 12, color: "1E293B", isTextBox: true, margin: 0 });
card(s, 0.5, 3.8, 9, 1.2, "FFF7ED");
s.addText([{ text: "Alcance: ", options: { bold: true, color: "C2410C" } },
  { text: "son datos de catálogo. No hay usuarios, reproducciones, suscripciones ni dispositivos, así que este análisis no responde retención ni engagement. Lo declaramos como limitación y pedimos esas tablas (mejora prioritaria)." }],
  { x: 0.65, y: 3.85, w: 8.7, h: 1.1, fontSize: 12, color: "1E293B", valign: "middle", isTextBox: true, margin: 0 });
s.addNotes("[1:00] Integración: unimos películas y series en un catálogo con clave uid porque show_id se repite. Cada decisión de limpieza está en reports/data_quality/cleaning_summary.csv. Dejar clara la limitación de alcance: sin datos de usuarios. Si el docente pregunta por retención o engagement: los datos entregados no lo permiten; es una limitación y un riesgo que declaramos.");

// 4 EDA
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "3. Análisis exploratorio: patrones y hallazgos", "Tres patrones que cambian cómo se decide");
stat(s, 0.5, 1.3, 2.1, "7,29", "calificación de series vs. 6,35 de películas", "F97316");
stat(s, 0.5, 2.7, 2.1, "0,23", "Spearman popularidad-calificación en películas (series: 0,17)");
stat(s, 0.5, 4.1, 2.1, "37%", "de las películas no recupera su presupuesto", "0D9488");
s.addChart(pres.charts.BAR, [{ name: "ROI (x)", labels: ["Agregado", "Mediano", "Promedio (≥ USD 10.000)"], values: [2.9, 1.7, 4.2] }],
  { x: 2.8, y: 1.3, w: 3.7, h: 3.9, barDir: "col", chartColors: ["2563EB"], showValue: true, dataLabelFormatCode: "0.0\"x\"", dataLabelPosition: "outEnd", dataLabelColor: "0F172A", dataLabelFontSize: 11,
    showTitle: true, title: "Tres formas de medir ROI (3.540 películas)", titleFontSize: 11, titleColor: "334155", showLegend: false,
    catAxisLabelColor: "334155", catAxisLabelFontSize: 10, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" } });
card(s, 6.7, 1.3, 2.8, 3.9);
s.addText([{ text: "Lectura", options: { bold: true, fontSize: 13, color: "0F172A", breakLine: true } },
  ...bullets(["Popularidad ≠ calidad", "Japón y Corea del Sur superan a EE. UU. dentro de cada tipo (comparar películas con películas)", "El promedio de ROI engaña: usar la mediana", "Serie temporal plana (1.000 por año): característica del extracto, no tendencia"], { paraSpaceAfter: 4 })],
  { x: 6.82, y: 1.4, w: 2.6, h: 3.7, fontSize: 11, color: "334155", valign: "top", isTextBox: true, margin: 0 });
s.addNotes("[1:10] Patrones: comparación (series vs. películas), relación (popularidad-calificación) y concentración/anomalías (ROI). Spearman por tipo y solo con títulos de 10 o más votos. Los tres ROI: agregado = ingresos totales / presupuesto total (el del dashboard); mediano = película típica; promedio inflado por pocos éxitos de bajo costo. Sin filtrar daba 781x por presupuestos cercanos a USD 1.");

// 5 JUSTIFICACIÓN GRÁFICOS
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "4. Justificación de las representaciones gráficas", "Cada gráfico responde una pregunta; cada atributo visual tiene una razón");
s.addTable([[hdr("Pregunta (patrón)"), hdr("Gráfico"), hdr("Atributo visual y por qué")],
  [cell("¿Qué predomina? (comparación)"), cell("Barras horizontales ordenadas"), cell("Longitud: el canal más preciso; nombres largos legibles. Torta descartada (83 idiomas)")],
  [cell("¿Cómo se distribuye? (distribución)"), cell("Histograma + boxplot por tipo"), cell("Muestra forma y extremos; escala log por la fuerte asimetría")],
  [cell("¿Se relacionan? (relación)"), cell("Dispersión con Spearman por tipo"), cell("Tamaño = votos (cuánta evidencia respalda el punto); Pearson descartado por asimetría")],
  [cell("¿Se recupera la inversión?"), cell("Dispersión log-log con línea ROI = 1"), cell("La línea separa ganancia de pérdida; ejes lineales aplastarían los puntos")],
  [cell("¿Dónde se concentra?"), cell("Mapa coroplético + barras Top 10"), cell("El mapa muestra el patrón, la barra la posición exacta")],
  [cell("¿Qué es inusual? (anomalías)"), cell("Strip plot con regla IQR"), cell("Destaca atípicos sin esconderlos")]],
  Object.assign({ x: 0.5, y: 1.3, w: 9, colW: [2.6, 2.6, 3.8], rowH: 0.5 }, TB));
s.addText([{ text: "Reglas transversales: ", options: { bold: true } }, { text: "azul = película y naranja = serie (siempre); paleta apta para daltonismo; eje desde cero; alcance visible bajo cada título." }],
  { x: 0.5, y: 4.75, w: 9, h: 0.5, fontSize: 11.5, color: "334155", isTextBox: true, margin: 0 });
s.addNotes("[1:00] IE26: justificar técnicamente. Responder siempre con tres elementos: pregunta analítica, tipo de variable y alternativa descartada. Ejemplo del eje: el gráfico de evolución tenía el eje cortado y una caída de 9 títulos parecía grande; lo corregimos.");

// 6 DASHBOARD
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "5. Dashboard interactivo", "KPIs, filtros, navegación e interacción (Streamlit + Plotly)");
s.addImage({ path: "images/dashboard/01_ejecutivo.png", x: 0.5, y: 1.3, w: 4.4, h: 2.93, sizing: { type: "contain", w: 4.4, h: 2.93 } });
s.addImage({ path: "images/dashboard/02_analitico.png", x: 5.1, y: 1.3, w: 4.4, h: 2.93, sizing: { type: "contain", w: 4.4, h: 2.93 } });
s.addText("Ejecutivo (Directorio)", { x: 0.5, y: 4.25, w: 4.4, h: 0.25, fontSize: 10, italic: true, color: "6B7280", align: "center", isTextBox: true, margin: 0 });
s.addText("Analítico (Contenidos y Adquisición)", { x: 5.1, y: 4.25, w: 4.4, h: 0.25, fontSize: 10, italic: true, color: "6B7280", align: "center", isTextBox: true, margin: 0 });
s.addText([{ text: "KPIs: ", options: { bold: true } }, { text: "títulos, países, géneros, nota, popularidad, presupuesto, ingresos, ROI.   " },
  { text: "Filtros: ", options: { bold: true } }, { text: "tipo, años, género (ejecutivo); + país, idioma, nota (analítico).   " },
  { text: "Navegación: ", options: { bold: true } }, { text: "portada y 3 vistas.   " },
  { text: "Interacción: ", options: { bold: true } }, { text: "tooltips, umbrales ajustables y exportación CSV." }],
  { x: 0.5, y: 4.55, w: 9, h: 0.7, fontSize: 11, color: "1E293B", isTextBox: true, margin: 0 });
s.addNotes("[0:45] Mostrar en vivo si hay tiempo: abrir Ejecutivo, cambiar el filtro a «TV Show» y ver cómo cambia la Lectura rápida. Comando: streamlit run dashboard/app.py.");

// 7 STORYTELLING
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "6. Narrativa visual (Data Storytelling)", "Arco en cinco escenas, adaptado a cada audiencia");
const esc = [["1", "Contexto", "Cada área mide distinto", "KPIs"], ["2", "Hallazgo", "Catálogo equilibrado; Drama y EE. UU. dominan", "Barras y mapa"],
             ["3", "Tensión", "Lo más popular no es lo mejor evaluado", "Dispersión"], ["4", "Evidencia", "Series 7,29; Asia sobresale; ROI mediano 1,7x", "Barras y finanzas"],
             ["5", "Acción", "Priorizar Asia; validar 349 casos de bajo presupuesto", "Tabla y conclusiones"]];
esc.forEach((e, i) => {
  const x = 0.5 + i * 1.82;
  card(s, x, 1.4, 1.7, 2.45);
  s.addShape(pres.shapes.OVAL, { x: x + 0.6, y: 1.5, w: 0.5, h: 0.5, fill: { color: i === 2 ? "F97316" : "2563EB" }, line: { color: "FFFFFF", width: 0 } });
  s.addText(e[0], { x: x + 0.6, y: 1.5, w: 0.5, h: 0.5, fontSize: 15, bold: true, color: "FFFFFF", align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText(e[1], { x: x + 0.05, y: 2.05, w: 1.6, h: 0.3, fontSize: 12.5, bold: true, color: "0F172A", align: "center", isTextBox: true, margin: 0 });
  s.addText(e[2], { x: x + 0.1, y: 2.4, w: 1.5, h: 0.95, fontSize: 10.5, color: "334155", align: "center", valign: "top", isTextBox: true, margin: 0 });
  s.addText(e[3], { x: x + 0.05, y: 3.45, w: 1.6, h: 0.3, fontSize: 10, italic: true, color: "2563EB", align: "center", isTextBox: true, margin: 0 });
});
s.addText([{ text: "Adaptación al público: ", options: { bold: true } }, { text: "el Directorio lee primero la «Lectura rápida» (conclusión) y baja al detalle solo si quiere; Contenidos explora con filtros; Data & Analytics audita la calidad. Oral, escrita y visual: frase de cierre por escena, título con alcance en cada gráfico y color con significado constante." }],
  { x: 0.5, y: 4.05, w: 9, h: 1.1, fontSize: 12, color: "1E293B", isTextBox: true, margin: 0 });
s.addNotes("[0:50] Contar la historia en orden: contexto, hallazgo, tensión, evidencia, acción. La tensión es popularidad vs. calidad; la acción son las recomendaciones de la diapositiva 11.");

// 8 FORTALEZAS
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "7. Evaluación crítica · Fortalezas con evidencia", "Cada fortaleza se puede verificar en el proyecto");
s.addTable([[hdr("Fortaleza"), hdr("Evidencia verificable"), hdr("Por qué importa")],
  [cell("Audiencia y decisión explícitas"), cell("3 vistas con audiencia declarada en la portada"), cell("Cada área ve lo que necesita")],
  [cell("Reglas de negocio visibles"), cell("Nota ≥ 10 votos, 0 = «sin dato», ROI definido en pantalla"), cell("El mismo indicador significa lo mismo")],
  [cell("Limpieza trazable"), cell("20 decisiones en cleaning_summary.csv"), cell("Los números se auditan")],
  [cell("Interacción útil"), cell("3 filtros (ejecutivo), 6 (analítico), umbrales ajustables, CSV"), cell("Explora sin pedir otro reporte")],
  [cell("Autocrítica verificable"), cell("6 mejoras antes→después y página de calidad"), cell("Muestra cuánta confianza merece cada cifra")],
  [cell("Reproducible"), cell("Corre desde copia limpia; datos incluidos"), cell("Otro equipo puede verificarlo")]],
  Object.assign({ x: 0.5, y: 1.3, w: 9, colW: [2.6, 3.7, 2.7], rowH: 0.5 }, TB));
s.addNotes("[0:45] IE31: cada fortaleza con evidencia concreta. Decisiones de diseño justificadas: Streamlit porque comparte pipeline Python; dos dashboards por audiencia; Spearman por tipo; percentil de popularidad dentro del tipo; calificación solo con 10 o más votos (con ceros el promedio bajaba de 6,63 a 5,69).");

// 9 LIMITACIONES, SESGOS, RIESGOS
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "8. Limitaciones, sesgos y riesgos, con mitigación", "Lo que el dato no permite y cómo reducimos el riesgo");
s.addTable([[hdr("Tipo"), hdr("Evidencia"), hdr("Mitigación")],
  [cell("Alcance", { bold: true }), cell("Solo catálogo: sin usuarios, reproducciones ni dispositivos"), cell("Declarar alcance; solicitar esas tablas; no inferir comportamiento")],
  [cell("Sesgo de cobertura", { bold: true }), cell("Solo 22% de películas con finanzas; son las más conocidas (mediana 1.007 votos vs. 101)"), cell("Rotular «solo con datos financieros»; usar ROI mediano")],
  [cell("Sesgo de selección", { bold: true }), cell("Nota solo con ≥ 10 votos: títulos más populares (11,1 vs. 9,4)"), cell("Umbral visible y ajustable; mostrar % con nota válida")],
  [cell("Sesgo de composición", { bold: true }), cell("Japón y Corea: 60-65% series, que puntúan más (7,29 vs. 6,35)"), cell("Comparar dentro de cada tipo; mostrar cobertura de nota")],
  [cell("Sesgo de origen", { bold: true }), cell("Inglés 43,7% y EE. UU. 34,2% de los títulos"), cell("Mínimo de títulos por país; comparar nota, no volumen")],
  [cell("Muestreo temporal", { bold: true }), cell("1.000 películas + 1.000 series por año"), cell("Advertencia y eje desde cero; sin tendencias")],
  [cell("Riesgo: atípicos", { bold: true }), cell("ROI sin filtrar de 781x por presupuestos ≈ USD 1"), cell("Filtro ≥ USD 10.000; pestaña de anomalías; validar en la fuente")],
  [cell("Riesgo: causalidad", { bold: true }), cell("Spearman 0,17 a 0,23"), cell("Advertencias; la decisión final es humana")]],
  Object.assign({ x: 0.5, y: 1.3, w: 9, colW: [1.7, 4, 3.3], rowH: 0.47 }, TB));
s.addNotes("[1:00] IE32 (17%): limitaciones, sesgos y riesgos CON medidas de mitigación. La más importante: son datos de catálogo, no de usuarios. El sesgo de cobertura se comprobó: las películas con datos financieros tienen mediana de 1.007 votos contra 101, y popularidad relativa 0,70 contra 0,44.");

// 10 MEJORAS
s = pres.addSlide({ masterName: "CONTENIDO" });
title(s, "9. Mejoras: implementadas y priorizadas", "Lo que ya cambió y lo que haríamos primero (impacto sobre esfuerzo)");
card(s, 0.5, 1.3, 4.3, 3.85);
s.addText([{ text: "Implementadas (se verifican en la ejecución)", options: { bold: true, fontSize: 12, color: "0D9488", breakLine: true } },
  ...bullets(["M1 Página «Calidad y EDA»", "M2 Cifras coherentes (6,63; Spearman; 3 ROI)", "M3 «Lectura rápida» en el ejecutivo", "M4 Exportar CSV de lo filtrado", "M5 Datos incluidos, notebook y README", "M6 Eje Y desde cero"], { paraSpaceAfter: 4 })],
  { x: 0.62, y: 1.38, w: 4.1, h: 3.7, fontSize: 11, color: "1E293B", valign: "top", isTextBox: true, margin: 0 });
s.addTable([[hdr("Prio."), hdr("Siguiente mejora"), hdr("Impacto / esfuerzo")],
  [cell("1", { bold: true }), cell("Pedir tablas de usuarios, reproducciones y mayor cobertura financiera"), cell("Alto / medio")],
  [cell("2", { bold: true }), cell("Pruebas automatizadas de limpieza y KPI"), cell("Alto / bajo")],
  [cell("3", { bold: true }), cell("Prueba de usabilidad con 3-5 usuarios"), cell("Alto / bajo")],
  [cell("4", { bold: true }), cell("Desplegar el dashboard en la web"), cell("Medio / bajo")],
  [cell("5", { bold: true }), cell("Revisión de accesibilidad"), cell("Medio / bajo")],
  [cell("6", { bold: true }), cell("Construir el .pbix de Power BI"), cell("Medio / medio")]],
  Object.assign({ x: 5.0, y: 1.3, w: 4.5, colW: [0.55, 2.55, 1.4], rowH: 0.5 }, TB));
s.addNotes("[0:50] IE33 (20%): mejoras viables, priorizadas y fundamentadas. La prioridad 1 es la de mayor impacto porque habilita retención y engagement, hoy imposibles. La 2 protege contra repetir el error de cifras distintas (M2). La priorización es juicio del equipo, no una medición. Después de esta diapositiva se hace la ejecución para revisar M1 a M6: Ejecutivo (Lectura rápida + CSV) y Calidad y EDA.");

// 11 RECOMENDACIONES, IMPACTO, CONCLUSIÓN
s = pres.addSlide({ masterName: "PORTADA" });
s.addText("10. Recomendaciones, impacto y conclusión", { x: 0.6, y: 0.3, w: 8.8, h: 0.55, fontSize: 26, bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
const rec = [["Decidir con popularidad Y calificación", "Spearman 0,17-0,23: una no predice la otra.", "Cambia: ya no se compra solo por popularidad"],
             ["Priorizar Asia; pilotos en México y Colombia", "Películas: Japón 6,90 y Corea 6,82 vs. EE. UU. 6,26; Colombia: solo 90 series.", "Cambia: se busca por rendimiento, no por volumen"],
             ["Usar el ROI mediano (1,7x) como referencia", "37% no recupera inversión; el promedio engaña.", "Cambia: una sola referencia de riesgo"],
             ["Validar 349 casos de bajo presupuesto con ROI ≥ 3", "Pueden ser errores de carga: verificar en la fuente.", "Cambia: no se invierte sobre un dato dudoso"]];
rec.forEach((r, i) => {
  const x = 0.6 + (i % 2) * 4.5, y = 1.05 + Math.floor(i / 2) * 1.5;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.3, h: 1.35, fill: { color: "1E293B" }, line: { color: "334155", width: 0.75 } });
  s.addText(r[0], { x: x + 0.12, y: y + 0.06, w: 4.06, h: 0.4, fontSize: 12.5, bold: true, color: "FDBA74", isTextBox: true, margin: 0 });
  s.addText(r[1], { x: x + 0.12, y: y + 0.46, w: 4.06, h: 0.45, fontSize: 10.5, color: "E2E8F0", isTextBox: true, margin: 0 });
  s.addText(r[2], { x: x + 0.12, y: y + 0.92, w: 4.06, h: 0.38, fontSize: 10.5, italic: true, color: "93C5FD", isTextBox: true, margin: 0 });
});
s.addText("Impacto esperado: la solución no decide por la organización, cambia qué evidencia ve quien decide y cuánta confianza merece. No estimamos ahorros porque no hay línea base; el impacto se medirá con la prueba de usabilidad y la adopción de los indicadores. Las limitaciones que quedan son del dato, no del diseño.",
  { x: 0.6, y: 4.1, w: 8.8, h: 1.2, fontSize: 12.5, color: "FFFFFF", isTextBox: true, margin: 0 });
s.addNotes("[1:00] IE35 (17%) e IE36 (20%): cada recomendación va con su evidencia, y el impacto se explica como cambio en la decisión, sin inventar cifras. Cierre: la solución muestra resultados y también cuánta confianza merecen. Total aproximado: 10 minutos. Quedan 5 para preguntas.");

(async () => {
  await pres.writeFile({ fileName: "docs/StreamView_Presentacion_EA3.pptx" });
  await applyTheme("docs/StreamView_Presentacion_EA3.pptx", THEME);
  console.log("ok");
})();
