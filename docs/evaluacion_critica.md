# Evaluación crítica de la solución (EA3)

> **Criterios.** La evaluación sigue los indicadores de la pauta EP6: fortalezas con evidencia, limitaciones, sesgos y riesgos con mitigación, mejoras priorizadas, recomendaciones justificadas e impacto esperado. La guía 3.1.1 aporta el criterio de que el EDA y la calidad de datos van antes del dashboard (mejora M1).

## 1. Fortalezas

| # | Fortaleza | Evidencia |
|---|---|---|
| F1 | Cada dashboard tiene una audiencia y una pregunta de negocio explícitas | `dashboard/app.py`, `docs/problema_negocio.md` |
| F2 | Reglas de negocio visibles en pantalla (nota con ≥ 10 votos, 0 = «sin dato», ROI definido) | expander de la portada, tooltips de los KPI |
| F3 | Decisiones de limpieza documentadas una a una (20 decisiones) | `reports/data_quality/cleaning_summary.csv` |
| F4 | Gráficos justificados por tipo de variable y pregunta | `docs/ea2_justificacion_graficos.md` |
| F5 | Filtros globales (tipo, años, género, país, idioma, calificación) que actualizan KPIs y gráficos | `dashboard/utils.py` |
| F6 | Paleta accesible (azul/naranja distinguibles para daltonismo) y alcance visible en cada vista | `dashboard/utils.py` |
| F7 | Pipeline reproducible con un comando | `notebooks/01_analisis_completo.py` |

## 2. Evaluación por tópico, limitaciones y mejora aplicada

| Tópico | Limitación detectada (antes) | Mejora implementada (después) |
|---|---|---|
| **Calidad y confiabilidad de los datos** | El dashboard mostraba resultados pero no cuán confiables eran: el usuario no veía datos faltantes ni valores atípicos | **M1** Página «Calidad y EDA» con faltantes por campo, distribuciones, correlaciones y anomalías de ROI |
| **Coherencia de los indicadores** | La documentación del EDA (EA1) tenía cifras distintas a las de los dashboards (nota 5,69 vs 6,63; correlación Pearson 0,03; ROI 4,2x vs 2,9x) y hablaba de «crecimiento sostenido» | **M2** Un solo criterio en todo el proyecto: `eda_complete.py` y `resultados_eda.md` alineados; ROI con 3 definiciones documentadas |
| **Narrativa / Data storytelling** | El dashboard ejecutivo mostraba KPIs y gráficos, pero la conclusión quedaba a cargo del lector | **M3** «Lectura rápida» dinámica en el ejecutivo: la conclusión aparece primero y cambia con los filtros |
| **Interacción y uso posterior** | No se podía llevar a Excel/Power BI lo que el usuario filtraba | **M4** Botón de descarga de los títulos filtrados (CSV) |
| **Elección de gráficos** | Correlación con Pearson sobre variables muy asimétricas y mezclando tipos; eje Y truncado en la evolución temporal (exageraba una caída de 9 títulos) | **M2** Spearman por tipo y solo sobre títulos con calificación válida; **M6** eje Y desde 0 |
| **Reproducibilidad** | `data/processed/` ignorado en git, sin notebook `.ipynb`, README con instrucciones solo para Windows | **M5** Datos procesados incluidos, notebook ejecutable, README multiplataforma y estructura documentada |
| **Accesibilidad** | Color como único canal en algunos gráficos | Paleta ya accesible; se mantienen etiquetas de datos y tooltips (mejora parcial, ver oportunidades) |
| **Ética y privacidad** | Riesgo de decidir adquisiciones solo con popularidad | Advertencias «correlación ≠ causalidad» y «validar con fuente» en la página de anomalías; ver `docs/etica_privacidad.md` |

## 3. Limitaciones, sesgos y riesgos, con mitigación

| Tipo | Descripción y evidencia | Riesgo para la decisión | Mitigación |
|---|---|---|---|
| Alcance | Solo datos de catálogo: sin usuarios, reproducciones, suscripciones ni dispositivos | Responder retención o engagement sin datos que lo sustenten | Declararlo; solicitar esas tablas (mejora prioridad 1) |
| Cobertura financiera | Solo 22% de las películas tiene finanzas y son las más conocidas (mediana de 1.007 votos vs. 101) | Generalizar el ROI a todo el catálogo | Mostrar siempre la cobertura; no extrapolar a series ni a títulos pequeños |
| Selección en la calificación | 64% de los títulos tiene ≥ 10 votos; en series solo 38% | Que «series mejor evaluadas» refleje solo las series conocidas | Mostrar cobertura junto a cada nota; comparar dentro de cada tipo |
| Composición | Japón y Corea del Sur tienen 60%-65% de series, que puntúan más (7,29 vs. 6,35) | Atribuir al país un efecto del tipo de contenido | Comparar dentro de cada tipo (películas 6,90 y 6,82 vs. 6,26 de EE. UU.) |
| Origen | EE. UU. es el 34,2% de los títulos; inglés 43,7% | Rankings dominados por volumen | Mínimo de títulos por país; comparar nota y popularidad relativa |
| Muestreo temporal | ≈1.000 películas y ≈1.000 series por año | Leer una tendencia inexistente | Advertencia en pantalla y eje Y desde 0 |
| Datos atípicos | ROI promedio sin filtrar de 781x (presupuestos cercanos a USD 1) | Invertir por un error de carga | Filtro ≥ USD 10.000, pestaña de anomalías, validar en la fuente |
| Interpretación | Spearman 0,17 a 0,23 | Confundir asociación con causalidad | Advertencias en pantalla; decisión humana final |

## 4. Oportunidades de mejora, priorizadas
Criterio: impacto sobre la decisión frente al esfuerzo. Es un juicio del equipo, no una medición.

| Prio. | Mejora | Impacto | Esfuerzo | Viabilidad |
|---|---|---|---|---|
| 1 | Solicitar usuarios, reproducciones, suscripciones, clasificación etaria y cobertura financiera | Alto | Medio (depende del proveedor) | Viable como requerimiento formal |
| 2 | Pruebas automatizadas de limpieza y KPI | Alto | Bajo | Evita repetir cifras distintas entre documentos |
| 3 | Prueba de usabilidad con 3 a 5 usuarios | Alto | Bajo | Aún no hay evidencia de uso real |
| 4 | Desplegar el dashboard en la web | Medio | Bajo | El código ya corre en Streamlit |
| 5 | Revisión de accesibilidad | Medio | Bajo | La paleta ya considera daltonismo |
| 6 | Construir el `.pbix` | Medio | Medio | El modelo y las medidas DAX ya existen |

## 5. Impacto esperado en la toma de decisiones
La solución no decide por la organización: cambia qué evidencia ve quien decide. No se estiman ahorros en cifras porque no se midieron.

| Decisión | Sin la solución | Con la solución | Cómo se mediría |
|---|---|---|---|
| Qué contenido adquirir | La popularidad sustituye a la calidad | Se ve que la relación es débil (Spearman 0,17-0,23) | Decisiones que citan ambas métricas |
| En qué mercados buscar | Domina el volumen | Se compara nota dentro de cada tipo y cobertura | Pilotos realizados y su nota posterior |
| Cuánto riesgo financiero asumir | ROI contradictorio entre reportes (781x, 4,2x, 2,9x) | Referencia única: mediana 1,7x y ≈37% no recupera | Definiciones distintas por KPI (meta: una) |
| Cuándo confiar en un dato | Cada área usa criterios propios | Una definición por indicador y página de calidad | Consultas de calidad resueltas con el dashboard |
