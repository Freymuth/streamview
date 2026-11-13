# Conclusiones y recomendaciones

## Hallazgos que sostienen las recomendaciones
1. **Catálogo equilibrado** (16.000 películas, 15.991 series) pero concentrado: Drama (14.773 títulos) y Estados Unidos (10.955).
2. **Popularidad ≠ calidad**: Spearman 0,23 (películas) y 0,17 (series). Un título muy buscado no es necesariamente bien evaluado.
3. **Series mejor evaluadas que películas**: 7,29 vs. 6,35 (sobre títulos con ≥ 10 votos).
4. **Japón y Corea del Sur** superan a EE. UU. dentro de cada tipo (películas 6,90 y 6,82 vs. 6,26; series 7,45 y 7,34 vs. 7,21). La nota agregada por país (7,22 y 7,10) exagera la diferencia porque esos catálogos tienen más series, que puntúan más. **México y Colombia** tienen poco volumen, pero sus series muestran popularidad relativa alta (0,69 y 0,63 vs. 0,57 de EE. UU.).
5. **Finanzas** (3.540 películas, 22% de las películas): ROI agregado 2,9x, ROI mediano 1,7x y ≈37% de las películas no recupera su presupuesto. Entre las películas del cuartil de menor presupuesto (≤ USD 6 M) hay 349 con ROI ≥ 3.

## Recomendaciones
| # | Recomendación | Evidencia | Cautela |
|---|---|---|---|
| R1 | No usar la popularidad como sustituto de la calidad al decidir adquisiciones; mirar ambas | Spearman 0,17-0,23 | Asociación, no causalidad |
| R2 | Priorizar adquisiciones de Japón y Corea del Sur y evaluar pilotos de series de México y Colombia | Dentro de cada tipo, Japón y Corea superan a EE. UU. en nota; series de México y Colombia con popularidad relativa 0,69 y 0,63 vs. 0,57 | Cobertura de nota de 53% a 77%; Colombia: 90 series |
| R3 | Dar prioridad a series de Sci-Fi & Fantasy y Action & Adventure (mejor nota) y a películas de Aventura, Acción y Fantasía (mayor popularidad relativa) | Géneros con ≥ 300 títulos | Popularidad es un índice relativo, no reproducciones |
| R4 | Explorar películas de bajo presupuesto con ROI alto, **validando primero el dato en la fuente** | 349 películas con presupuesto ≤ USD 6 M y ROI ≥ 3 | Los ROI extremos pueden ser errores de carga |
| R5 | Usar el ROI mediano (1,7x) y el % que no recupera inversión (≈37%) como referencia de riesgo, no el promedio | `reports/eda/roi_definiciones.csv` | Solo 22% de las películas tiene datos financieros |
| R6 | Mejorar la fuente de datos: clasificación etaria, reproducciones reales, más cobertura financiera | Limitaciones del extracto | Requiere al proveedor |
| R7 | Unificar los indicadores en estos dashboards como versión única de la verdad | Problema de negocio: múltiples versiones del mismo KPI | Requiere gobierno de datos |

Los resultados describen asociaciones y no deben automatizar decisiones de adquisición sin criterio humano (`docs/etica_privacidad.md`).
