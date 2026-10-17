# EA2 · Justificación de diseño y limitaciones

Cada visualización se justifica por **tipo de dato**, **audiencia** y **propósito comunicacional** (regla de negocio 8).
Paleta única: azul = película / valor principal, naranja = serie / segunda serie. Sin gráficos 3D, sin adornos.

## Dashboard Ejecutivo (Directorio y Gerencia General)

| Visualización | Tipo de dato | Propósito | Por qué este gráfico |
|---|---|---|---|
| 8 KPIs (títulos, películas, series, países, idiomas, géneros, popularidad, calificación) | Totales y promedios | Estado del catálogo en 5 segundos | Un número grande se lee más rápido que cualquier gráfico. |
| Áreas: estrenos e incorporación por año | Serie temporal, conteo | ¿Cómo evolucionó el catálogo? | El área comunica volumen acumulado en el tiempo; dos series superpuestas con transparencia permiten comparar estreno vs. incorporación. |
| Barra simple película vs. serie | Categórica (2 niveles) | Composición del catálogo | Con 2 categorías, barras con etiqueta directa evitan la ambigüedad de un gráfico circular. |
| Mapa coroplético de producciones | Geográfico, conteo | Dónde se produce | Responde la pregunta geográfica de un vistazo; el color secuencial azul indica magnitud. |
| Barras Top 10 países | Categórica ordenada | Ranking exacto | El mapa muestra patrón, la barra muestra posiciones exactas. |
| Barras Top 10 géneros / idiomas | Categórica ordenada | Qué predomina | Barras horizontales: los nombres largos se leen mejor y la longitud es la codificación más precisa. |
| Filtros: tipo, años, género | — | Explorar sin saturar | Pocos filtros para una audiencia ejecutiva. |

## Dashboard Analítico (Gerencia de Contenidos y Adquisición)

| Visualización | Tipo de dato | Propósito | Por qué este gráfico |
|---|---|---|---|
| Dispersión popularidad vs. calificación (tamaño = votos, color = tipo) | 2 numéricas + 1 numérica + 1 categórica | ¿Existe relación? | La dispersión es el gráfico estándar para relación entre dos variables; escala log en popularidad por su fuerte asimetría. |
| Correlación de Spearman **por tipo** | Estadístico | Cuantificar la relación | Spearman por ser monótona y robusta a outliers; por tipo porque mezclar escalas distintas la distorsiona. |
| Top 10 mejor evaluados (umbral de votos) | Categórica ordenada | Contenidos de referencia | Umbral configurable (por defecto 500 votos) evita que títulos con 1-2 votos dominen. |
| Barras popularidad y calificación por género | Categórica × 2 métricas | Qué géneros rinden | Dos paneles con eje Y compartido (escalas distintas, mismo orden). |
| Treemap de géneros (D3 / Plotly) | Jerárquica/part-to-whole | Peso de cada género | El área expresa participación en el total; color = calificación aporta una 2ª variable. |
| Mapa de calificación/popularidad por país | Geográfico, promedio | Mercados de oportunidad | Con mínimo de títulos válidos (configurable) para que el promedio sea confiable. |
| Top directores y actores | Categórica ordenada | Talento recurrente | Barras: ranking exacto. |
| Dispersión presupuesto vs. ingresos (log-log) con línea ROI = 1 | 2 numéricas | ¿Existe relación? ¿Se recupera la inversión? | Log-log por rango de varios órdenes de magnitud; la línea de equilibrio hace evidente qué películas pierden dinero. |
| KPIs financieros | Totales | Panorama de inversión | Presupuesto promedio, total presupuesto, total ingresos y ROI aproximado (ingresos / presupuesto). |
| Top 10 por ingresos | Categórica ordenada | Grandes taquillas | Barras horizontales en millones de USD. |
| Tabla «éxitos con presupuesto reducido» | Tabla | Casos accionables | Umbrales (percentil de presupuesto y ROI) ajustables; se muestran números exactos. |
| Pestaña Conclusiones | Texto calculado | Responder las 4 preguntas del encargo | Lectura automática: se actualiza con los filtros. |

## Limitaciones (a declarar en la presentación)

1. **Clasificación etaria no disponible.** El campo `rating` del extracto es numérico e idéntico a `vote_average` (100% de coincidencia); no contiene TV-MA, PG-13, etc. El filtro solicitado aparece deshabilitado con explicación.
2. **Distribución uniforme por año.** El extracto tiene ≈2.000 títulos por año (2010–2025), por lo que la serie temporal es plana. Es una característica del dato, no un hallazgo de negocio; el dashboard lo advierte.
3. **Calificación solo con ≥ 10 votos.** El 36% del catálogo (11.660 títulos) queda sin calificación válida. Por eso el promedio global es 6,63, distinto del 5,69 del informe EA1 (que incluía 4.560 títulos con 0 votos como si fueran nota 0).
4. **Popularidad de series y películas en escalas distintas.** Para rankings combinados se usa el percentil dentro del tipo.
5. **Datos financieros solo para 3.540 de 16.000 películas** (22%) y ausentes en series. Todo KPI financiero lo indica con una nota visible.
6. **Presupuestos no realistas.** 15 películas con presupuesto menor a USD 10.000 se excluyen de los rankings de éxito.
7. **Asociación, no causalidad.** Las lecturas automáticas describen patrones, no causas.
