# Power BI · Guía para armar el dashboard (EA2)

> Power BI Desktop (solo Windows) genera el archivo `.pbix`; yo no puedo crearlo por ti. Este repositorio trae todo lo demás listo:
> los datos limpios en modelo estrella, las consultas de Power Query, las 24 medidas DAX y un tema de colores.

| Archivo | Para qué |
|---|---|
| `data/*.csv` | 7 tablas (película **y** serie, géneros/países ya separados, `uid`, calificación limpia) |
| `consultas_power_query.m` | Carga de los CSV con tipos correctos |
| `medidas.dax` | Todas las medidas, listas para copiar y pegar |
| `StreamView_tema.json` | Tema de colores (azul = principal, naranja = series) |

## Por qué conviene rehacer el archivo (y no arreglar el anterior)
El `.pbix` actual carga **solo las películas crudas** (16.000), por lo que `Total Series` da 0. Además `country` y `genres` no están
separados (1.474 y 2.771 combinaciones distintas), de modo que el mapa y el treemap cuentan combinaciones como si fueran países o géneros.
Tiene 9 páginas con un visual cada una, y la ruta apunta a `C:\Users\MA-Alumno\Desktop\...`, que no existe en otros computadores.
Lo más rápido es un archivo nuevo: **Archivo → Guardar como `StreamView_EA2.pbix`** y empezar desde el paso 1.

## Paso 1 · Parámetro y datos
1. **Inicio → Transformar datos → Administrar parámetros → Nuevo**: nombre `RutaDatos`, tipo *Texto*, valor = ruta de **tu** carpeta `powerbi\data\` **con barra final**
   (ej. `C:\Users\chris\streamview-analytics\powerbi\data\`).
2. Por cada tabla: **Nueva fuente → Consulta en blanco → Editor avanzado**, pegar la consulta correspondiente de `consultas_power_query.m` y
   renombrar la consulta con el nombre de la tabla (`fact_catalogo`, `fact_financiero`, `bridge_genero`, `bridge_pais`, `bridge_director`, `bridge_actor`, `dim_calendario`).
3. **Cerrar y aplicar.**

> Las consultas fuerzan la cultura `en-US` al convertir tipos. Sin eso, tu Windows (es-CL, coma decimal) leería `6.63` como `663`.

## Paso 2 · Relaciones (vista de modelo)
| Desde (muchos) | Hacia (uno) | Filtro cruzado |
|---|---|---|
| `bridge_genero[uid]` | `fact_catalogo[uid]` | **Ambos** |
| `bridge_pais[uid]` | `fact_catalogo[uid]` | **Ambos** |
| `bridge_director[uid]`, `bridge_actor[uid]` | `fact_catalogo[uid]` | Único |
| `fact_financiero[uid]` | `fact_catalogo[uid]` | Ambos (uno a uno) |
| `fact_catalogo[anio_estreno]` | `dim_calendario[anio]` | Único (activa) |
| `fact_catalogo[anio_incorporacion]` | `dim_calendario[anio]` | Único (**inactiva**, la usa la medida `Incorporados`) |

«Ambos» en géneros y países permite que una segmentación por género o país filtre todo el resto.

## Paso 3 · Medidas y tema
- Copia cada medida de `medidas.dax` con **Modelado → Nueva medida** (conviene crear antes una tabla vacía `Medidas`).
- **Vista → Temas → Examinar temas** → `StreamView_tema.json`.

## Paso 4 · Valores de control
Cuando las tarjetas muestren estos valores, el modelo está bien:

| Medida | Valor esperado |
|---|---|
| Total Contenidos / Películas / Series | 31.991 / 16.000 / 15.991 |
| Países / Idiomas / Géneros | 147 / 83 / 27 |
| Popularidad Promedio | 42,6 |
| Calificación Promedio | 6,63 (con 20.331 títulos con calificación) |
| Estrenos 2015 / Incorporados 2015 | 2.000 / 2.000 |
| Películas con Datos Financieros | 3.540 (22,1%) |
| Presupuesto Promedio / Total Presupuesto / Total Ingresos | USD 35,6 M / 125.961 M / 367.371 M |
| ROI Aproximado / ROI Mediano | 2,92x / 1,70x |
| Top país (títulos) | EE. UU. 10.955 · Japón 2.869 · Reino Unido 2.608 |

## Paso 5 · Página 1 «Ejecutivo» (lienzo 1280 × 720)
| Visual | Campos | Posición (x, y, ancho × alto) |
|---|---|---|
| Segmentación Tipo | `fact_catalogo[tipo]` (botones) | 20, 70, 240 × 50 |
| Segmentación Años | `fact_catalogo[anio_estreno]` (entre) | 270, 70, 360 × 50 |
| Segmentación Género | `bridge_genero[genero]` (desplegable) | 640, 70, 300 × 50 |
| 8 tarjetas | Total Contenidos, Total Peliculas, Total Series, Paises, Idiomas, Generos, Popularidad Promedio, Calificacion Promedio | y = 130, alto 80, ancho 148, x = 20 + 156·i |
| Gráfico de áreas | Eje `dim_calendario[anio]`; valores `Estrenos` e `Incorporados` | 20, 225, 560 × 235 |
| Barras Top 10 países | Eje `bridge_pais[pais]`; valor `Total Contenidos`; filtro *N superior* = 10 | 590, 225, 330 × 235 |
| Barras película vs. serie | Eje `fact_catalogo[tipo]`; valor `Total Contenidos` | 930, 225, 330 × 235 |
| Mapa coroplético | Ubicación `bridge_pais[pais]`; saturación `Total Contenidos` | 20, 470, 560 × 235 |
| Barras Top géneros | Eje `bridge_genero[genero]`; valor `Total Contenidos`; *N superior* = 10 | 590, 470, 330 × 235 |
| Barras Top idiomas | Eje `fact_catalogo[idioma]`; valor `Total Contenidos`; *N superior* = 10 | 930, 470, 330 × 235 |

Agrega un cuadro de texto: *«Período y alcance: según los filtros activos. El extracto tiene 1.000 películas y 1.000 series por año, sin tendencia de crecimiento.»*

## Paso 6 · Página 2 «Analítico» (financiero incluido)
| Visual | Campos / configuración |
|---|---|
| Segmentaciones | tipo, género, país (`bridge_pais[pais]`), idioma, años, rango de `calificacion` |
| Dispersión popularidad vs. calificación | X `popularidad_percentil`, Y `calificacion`, tamaño `votos`, leyenda `tipo` |
| Barras por género | Eje `bridge_genero[genero]`; valores `Popularidad Promedio` y `Calificacion Promedio` |
| Treemap de géneros | Grupo `bridge_genero[genero]`; valores `Total Contenidos` |
| Top 10 mejor evaluados | Eje `fact_catalogo[titulo]`; valor `Calificacion Promedio`; filtro del visual `Votos Totales` ≥ 500 y *N superior* = 10 |
| Top directores / actores | `bridge_director[director]` con `Titulos por Director`; `bridge_actor[actor]` con `Titulos por Actor`; *N superior* = 10 |
| Mapa de calificación | Ubicación `bridge_pais[pais]`; valor `Calificacion Pais Confiable` |
| Dispersión presupuesto vs. ingresos | `fact_financiero[presupuesto]` × `[ingresos]`, ambos ejes en escala **logarítmica** |
| Top películas por ingresos | `fact_financiero[titulo]` con `Total Ingresos`; *N superior* = 10 |
| 4 tarjetas financieras | `Presupuesto Promedio`, `Total Presupuesto`, `Total Ingresos`, `ROI Aproximado` |
| **Nota visible** | Tarjeta con la medida `Nota Financiera` (exigencia del encargo 3.g.iv) |

> No incluyas filtro de clasificación etaria: el dato no existe (el campo `rating` duplica `vote_average`). Declara esa limitación en la presentación.

## Problemas frecuentes
- **El mapa no muestra países:** en `bridge_pais[pais]`, *Herramientas de columna → Categoría de datos → País o región*.
- **Un filtro de género no cambia el resto:** revisa que la relación `bridge_genero → fact_catalogo` tenga filtro cruzado **Ambos**.
- **Promedios 100 veces más grandes:** faltó la cultura `en-US` en la consulta (paso 1).
- **`Incorporados` sale igual que `Estrenos`:** la relación `anio_incorporacion → dim_calendario` debe quedar **inactiva**.
