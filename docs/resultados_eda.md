# Resultados del análisis exploratorio

Script: [`src/analysis/eda_complete.py`](../src/analysis/eda_complete.py)
Imágenes: [`images/eda/`](../images/eda/) · Tablas de respaldo: [`reports/eda/`](../reports/eda/)

## Datos analizados

31.991 títulos del catálogo unificado (`data/processed/catalogo_limpio.csv`),
estrenados entre 2010 y 2025.

## 1. Estructura del catálogo

- El catálogo está prácticamente empatado entre **16.000 películas (50,0%)**
  y **15.991 series (50,0%)** — `images/eda/01_distribucion_tipo.png`.
- Los géneros predominantes son **Drama** (14.773 títulos), **Comedy** (9.106) y
  **Animation** (4.070), sobre un total de 28 géneros distintos —
  `images/eda/02_generos_predominantes.png`.
- El catálogo tiene representación de **147 países**, liderado por
  Estados Unidos (10.955 títulos), Japón (2.869) y Reino Unido (2.608) —
  `images/eda/03_paises.png`.
- Se identifican **83 idiomas**; el inglés concentra la mayoría del catálogo —
  `images/eda/04_idiomas.png`.

## 2. Popularidad y valoración

- La popularidad normalizada (`popularity_norm`) permite comparar películas y
  series en la misma escala (0-1), controlando por el hecho de que sus rangos
  de popularidad originales no son comparables — `images/eda/05_comparativa_popularidad.png`.
- La calificación promedio del catálogo es **5,69 sobre 10**, y la popularidad
  promedio es **42,63** (índice relativo TMDB, no representa reproducciones).
- La correlación entre popularidad y calificación es **0,03** — prácticamente
  nula. Esto es un hallazgo relevante: un contenido puede ser muy buscado
  (popular) sin ser necesariamente bien evaluado por la audiencia, y viceversa
  — `images/eda/06_popularidad_vs_calificacion.png`.

## 3. Evolución temporal

El catálogo muestra una tendencia de crecimiento sostenido en el número de
estrenos incorporados año a año entre 2010 y 2025, tanto en películas como en
series — `images/eda/07_evolucion_historica.png`. El detalle año por año está
en `reports/eda/evolucion_historica.csv`.

## 4. Análisis financiero (solo películas con datos completos)

- Solo **3.540 de 31.991 títulos (11%)** tienen presupuesto e ingresos
  conocidos; todo lo que sigue se calcula únicamente sobre ese subconjunto.
- Presupuesto promedio: **USD 35,6 millones**. Ingresos totales acumulados:
  **USD 367.371 millones**.
- La relación presupuesto-ingresos es visible en
  `images/eda/08_presupuesto_vs_ingresos.png`: la mayoría de los puntos caen
  sobre la línea de equilibrio (ingresos = presupuesto) o por encima, lo que
  sugiere que, en promedio, las películas con datos financieros completos
  recuperan su inversión.
- **Advertencia sobre el ROI**: un pequeño número de películas tiene
  presupuestos declarados extremadamente bajos (cercanos a USD 1), lo que
  produce valores de ROI artificialmente enormes (ROI promedio sin filtrar:
  **781x**). Al excluir presupuestos menores a USD 10.000 —probablemente datos
  mal cargados o placeholders—, el ROI promedio baja a un valor mucho más
  creíble de **4,2x**. El ranking de Top 15 ROI
  (`images/eda/09_top_roi.png`, `reports/eda/top_roi.csv`) usa este filtro.

## Limitaciones

- `popularity` es un índice relativo entregado por la fuente (estilo TMDB); no
  debe interpretarse como número de reproducciones ni de suscriptores.
- El análisis financiero cubre solo el 11% del catálogo (las películas con
  datos completos); no es representativo del catálogo completo ni de las series.
- Los resultados son descriptivos y no permiten afirmar causalidad (por
  ejemplo, que un género "cause" mayor popularidad).
