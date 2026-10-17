# StreamView Analytics — Visual Analytics del catálogo audiovisual (EA1)

Proyecto académico para la asignatura Visualización de Datos (ADY1104, Duoc UC)
— caso semestral StreamView Analytics.

## Estado del proyecto

El repositorio incluye:

- comprensión del problema de negocio y stakeholders;
- codificación y preparación de datos (limpieza, duplicados, nulos, outliers);
- reglas de negocio (filtrado financiero, normalización, KPIs derivados);
- análisis exploratorio con las 8 visualizaciones requeridas por el caso;
- dashboard interactivo con filtros dinámicos;
- documentación de decisiones y limitaciones.

El detalle completo está en [`docs/`](docs/): [`problema_negocio.md`](docs/problema_negocio.md),
[`limpieza_datos.md`](docs/limpieza_datos.md), [`resultados_eda.md`](docs/resultados_eda.md)
y [`etica_privacidad.md`](docs/etica_privacidad.md).

## Problema de negocio

> ¿Qué caracteriza al catálogo audiovisual de StreamView Analytics, qué
> contenido genera más interés y valoración, y qué evidencia financiera
> respalda las decisiones de adquisición de nuevas películas?

## Fuente de datos

- Dataset oficial del caso: `netflix_movies_detailed_up_to_2025.csv` (16.000
  películas) y `netflix_tv_shows_detailed_up_to_2025.csv` (16.000 series).
- Archivos utilizados: `data/raw/`.
- No se reemplaza ni modifica su estructura original (requisito del caso).

## Resultados principales

- Catálogo unificado: 31.991 títulos (16.000 películas + 15.991 series tras
  eliminar duplicados).
- 147 países, 83 idiomas y 28 géneros representados.
- Géneros predominantes: Drama, Comedy, Animation.
- Popularidad promedio: 42,63. Calificación promedio: 5,69/10.
- Correlación popularidad-calificación: prácticamente nula (0,03) — ser
  popular no implica estar bien evaluado, ni viceversa.
- Solo el 11% del catálogo (3.540 títulos) tiene datos financieros completos;
  ROI promedio de ese subconjunto: 4,2x (excluyendo presupuestos irreales
  menores a USD 10.000).

Los resultados describen asociaciones, no causalidad.

## Estructura

```text
streamview-analytics/
|-- data/
|   |-- raw/                  # datasets oficiales del caso (sin modificar)
|   `-- processed/            # catalogo_limpio.csv, catalogo_financiero.csv
|-- docs/
|   |-- problema_negocio.md
|   |-- limpieza_datos.md
|   |-- resultados_eda.md
|   `-- etica_privacidad.md
|-- images/
|   `-- eda/                  # las 8 visualizaciones requeridas (PNG)
|-- notebooks/
|   `-- 01_analisis_completo.py
|-- reports/
|   |-- data_quality/         # decisiones de limpieza documentadas
|   `-- eda/                  # tablas de respaldo de cada gráfico
|-- dashboard/
|   `-- app.py                # dashboard interactivo (Streamlit + Plotly)
|-- src/
|   |-- data/clean_data.py    # limpieza + reglas de negocio
|   `-- analysis/eda_complete.py  # las 8 visualizaciones + reportes
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Instalación

```bash
uv venv
.venv\Scripts\Activate.ps1      # Windows
uv pip install -r requirements.txt
```

## Reproducción

Flujo completo (limpieza + gráficos) en un solo paso:

```bash
python notebooks/01_analisis_completo.py
```

O por etapas:

```bash
python src/data/clean_data.py       # genera data/processed/ y reports/data_quality/
python src/analysis/eda_complete.py # genera images/eda/ y reports/eda/
```

Dashboard interactivo:

```bash
streamlit run dashboard/app.py
```

(si `data/processed/` no existe aún, el dashboard genera los datos
automáticamente al iniciar).

## Metodología

El proyecto sigue las etapas del caso semestral: comprensión del negocio,
preparación de datos, reglas de negocio, análisis exploratorio, storytelling
en informe ejecutivo (EA1), dashboard interactivo (EA2) y cierre con
presentación ejecutiva (EA3). No incluye modelamiento predictivo ni
inteligencia artificial: es explícitamente un problema de Visual Analytics
descriptivo, no de Machine Learning.

## Ética y uso responsable

`popularity` no equivale a calidad ni a éxito comercial, la cobertura
geográfica y financiera del catálogo es desigual, y el análisis no debe
usarse para automatizar decisiones de adquisición o promoción sin criterio
humano. Detalle en [`docs/etica_privacidad.md`](docs/etica_privacidad.md).

## Limitaciones

- El análisis financiero cubre solo el 11% del catálogo.
- `popularity` es un índice relativo de una fuente externa, no vistas reales.
- Un pequeño número de presupuestos declarados es irrealmente bajo y se
  excluyó del ranking de ROI para evitar valores distorsionados.
- No se ha construido aún el storytelling final ni la presentación ejecutiva
  (siguiente paso del proyecto).
