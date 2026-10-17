# Guía Power BI (EA2)

> Power BI genera archivos `.pbix` solo desde **Power BI Desktop (Windows)**; este repositorio entrega el modelo de datos
> listo (`powerbi/data/*.csv`) y esta guía con las medidas DAX. Guarda tu archivo como `powerbi/StreamView.pbix`.

## 1. Cargar los datos
1. *Obtener datos → Texto/CSV* y carga los 7 archivos de `powerbi/data/`.
2. Verifica tipos: `popularidad`, `calificacion`, `presupuesto`, `ingresos`, `roi` = Número decimal; `anio_*`, `votos` = Número entero; `iso3` y `pais` = Texto.
3. En `bridge_pais`, columna `pais` → *Categoría de datos = País/Región* (para el mapa).

## 2. Relaciones (Vista de modelo)
| Desde (muchos) | Hacia (uno) | Dirección |
|---|---|---|
| `bridge_genero[uid]`, `bridge_pais[uid]`, `bridge_director[uid]`, `bridge_actor[uid]` | `fact_catalogo[uid]` | Única (de fact hacia puentes) |
| `fact_financiero[uid]` | `fact_catalogo[uid]` | Uno a uno, bidireccional |
| `fact_catalogo[anio_estreno]` | `dim_calendario[anio]` | Muchos a uno |

Para que un filtro por género/país afecte al resto, usa **filtro cruzado bidireccional** en `bridge_genero` y `bridge_pais` hacia `fact_catalogo`.

## 3. Medidas DAX (tabla `fact_catalogo` salvo indicación)
```DAX
Total Contenidos = COUNTROWS(fact_catalogo)
Total Peliculas  = CALCULATE([Total Contenidos], fact_catalogo[tipo] = "Película")
Total Series     = CALCULATE([Total Contenidos], fact_catalogo[tipo] = "Serie")
Paises           = DISTINCTCOUNT(bridge_pais[pais])
Idiomas          = DISTINCTCOUNT(fact_catalogo[idioma])
Generos          = DISTINCTCOUNT(bridge_genero[genero])
Popularidad Prom = AVERAGE(fact_catalogo[popularidad])
Calificacion Prom = AVERAGE(fact_catalogo[calificacion])   -- ya viene vacía si < 10 votos

-- Financieras (tabla fact_financiero)
Presupuesto Prom   = AVERAGE(fact_financiero[presupuesto])
Total Presupuesto  = SUM(fact_financiero[presupuesto])
Total Ingresos     = SUM(fact_financiero[ingresos])
ROI Aprox          = DIVIDE([Total Ingresos], [Total Presupuesto])
Peliculas Financieras = COUNTROWS(fact_financiero)

-- Mínimo de títulos por país (evita promedios poco confiables)
Calif Pais Confiable =
VAR n = CALCULATE(COUNTROWS(FILTER(fact_catalogo, NOT ISBLANK(fact_catalogo[calificacion]))))
RETURN IF(n >= 20, [Calificacion Prom], BLANK())
```

## 4. Páginas y visuales
**Página 1 · Ejecutivo:** 8 tarjetas (KPIs) · gráfico de áreas (`dim_calendario[anio]` × `Total Contenidos`) · barras Top 10 países (filtro *N superior* = 10) · barras Top géneros · barras película vs. serie · **mapa coroplético** (`bridge_pais[pais]`, saturación = `Total Contenidos`) · segmentaciones: tipo, rango de años, género.

**Página 2 · Analítico:** dispersión (`Popularidad Prom` × `Calificacion Prom`, tamaño = votos, leyenda = tipo) · barras por género (2 medidas) · **treemap** de géneros · Top 10 mejor evaluados (filtro `votos` ≥ 500) · Top directores/actores (*N superior* = 10) · mapa con `Calif Pais Confiable` · bloque financiero: dispersión presupuesto × ingresos, Top películas por ingresos, tarjetas (`Presupuesto Prom`, `Total Presupuesto`, `Total Ingresos`, `ROI Aprox`) y un **cuadro de texto visible**: *«Este análisis solo incluye películas con presupuesto e ingresos informados.»* · segmentaciones: tipo, género, país, idioma, años, rango de calificación.

> La clasificación etaria no existe en los datos; no la incluyas (ver `docs/ea2_justificacion_graficos.md`).

## 5. Estilo
Paleta: azul `#2563EB` (película / principal), naranja `#F97316` (serie). Fondo blanco, títulos claros en cada visual, sin 3D.
Configura *Ver → Tema* y usa el mismo tema en ambas páginas.
