# Limpieza y preparación de datos

Script: [`src/data/clean_data.py`](../src/data/clean_data.py)
Reporte generado: [`reports/data_quality/cleaning_summary.csv`](../reports/data_quality/cleaning_summary.csv)

## Decisiones aplicadas

| Campo | Problema detectado | Decisión | Justificación |
|---|---|---|---|
| `rating` | Idéntica a `vote_average` en el 100% de los registros (TV y Movies) | Eliminada | Columna duplicada, no aporta información nueva |
| `duration` (Movies) | 100% de valores nulos | Eliminada | Sin información utilizable |
| `date_added` | Texto, no fecha | Convertida a `datetime` | Permite operaciones temporales correctas |
| `show_id` | 9 duplicados en TV Shows, 0 en Movies | `drop_duplicates(keep="first")` | Cada registro debe representar un único contenido (regla de negocio del caso) |
| `director`, `cast`, `country`, `genres`, `description` | Nulos entre 1% y 20% según columna | Rellenados con `"Desconocido"` | Se prioriza no perder datos válidos de otras columnas de la misma fila |
| `budget` / `revenue` en 0 | ~70% y ~65% de las películas, respectivamente | Tratados como valor no disponible (`NaN`), no como costo/ingreso real de 0 | Un presupuesto de USD 0 no es plausible; el patrón es típico de bases de datos tipo TMDB donde 0 significa "dato no capturado" |

## Unificación del catálogo

`TV Shows` no tiene `budget` ni `revenue` (regla de negocio: esas variables son
exclusivas de películas). Para poder unir ambos datasets en un solo catálogo
corporativo, esas columnas se agregan a TV Shows como valores nulos, no como
cero — así ningún cálculo posterior las confunde con "sin costo".

Resultado: **31.991 títulos** unificados (16.000 películas + 15.991 series, tras
eliminar los 9 duplicados).

## Catálogo financiero (filtrado)

Se genera un segundo dataset, `data/processed/catalogo_financiero.csv`, que
conserva solo los títulos con `budget` **y** `revenue` conocidos. De los 31.991
títulos del catálogo, únicamente **3.540 (11%)** cumplen esta condición — el resto
son series (sin esa información por diseño) o películas con datos financieros
no disponibles. Todo el análisis de presupuesto, ingresos y ROI se calcula
exclusivamente sobre este subconjunto.

## Normalización

`popularity` no es comparable directamente entre películas y series (las
escalas de referencia son distintas). Se agrega `popularity_norm`, una
normalización min-max calculada de forma independiente dentro de cada tipo
(`Movie` / `TV Show`), para permitir comparaciones justas de "qué tan popular
es este título respecto a los de su misma categoría".
