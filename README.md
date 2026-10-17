# StreamView Analytics — Visual Analytics del catálogo audiovisual (EA1 + EA2)

Proyecto académico de Visualización de Datos (ADY1104, Duoc UC) — caso semestral StreamView Analytics.

| Etapa | Entregable | Estado |
|---|---|---|
| EA1 | Informe ejecutivo + EDA (8 visualizaciones) | ✅ [`docs/resultados_eda.md`](docs/resultados_eda.md) |
| **EA2** | **Dashboards interactivos (Ejecutivo y Analítico) + integración Python / D3 / Power BI** | ✅ este repositorio |
| EA3 | Evaluación crítica y rediseño | pendiente |

## EA2 — Qué incluye

| Requerimiento | Dónde está |
|---|---|
| Dashboard **Ejecutivo** (Directorio y Gerencia General) | `dashboard/pages/1_Ejecutivo.py` |
| Dashboard **Analítico** (Contenidos y Adquisición) con análisis financiero | `dashboard/pages/2_Analitico.py` |
| Python: **Streamlit, Dash, Matplotlib, Seaborn** | `dashboard/`, `dash_app/`, `src/analysis/` |
| **D3** | `src/d3_treemap.py` (incrustado en Streamlit) y `d3/treemap_generos.html` |
| **Power BI** | `powerbi/` (modelo en estrella + guía paso a paso con DAX) |
| Formato, estilos, leyendas, justificación de diseño | [`docs/ea2_justificacion_graficos.md`](docs/ea2_justificacion_graficos.md) |
| Gitflow + documentación técnica | [`docs/gitflow.md`](docs/gitflow.md), [`docs/ea2_arquitectura.md`](docs/ea2_arquitectura.md) |
| Presentación (arquitectura y herramientas) | [`docs/ea2_guion_presentacion.md`](docs/ea2_guion_presentacion.md) |

## Instalación

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1          # Windows (PowerShell)
pip install -r requirements.txt
```

## Ejecución (desde la raíz del proyecto)

```bash
python src/data/clean_data.py                 # genera data/processed/ y reports/data_quality/
streamlit run dashboard/app.py                # dashboards Ejecutivo y Analítico
python dash_app/app.py                        # dashboard financiero en Dash (http://127.0.0.1:8050)
python src/export/build_d3.py                 # d3/treemap_generos.html
python src/export/export_powerbi.py           # powerbi/data/*.csv
python src/analysis/eda_seaborn.py            # images/eda/10_*.png y 11_*.png
```

Todo el flujo (limpieza, EDA, Seaborn, D3, Power BI) en un paso: `python notebooks/01_analisis_completo.py`.
Si `data/processed/` no existe, los dashboards lo generan solos al iniciar.

## Estructura

```text
streamview-analytics/
|-- data/raw/                  # datasets oficiales (sin modificar)
|-- data/processed/            # catalogo_limpio.csv, catalogo_financiero.csv (generados)
|-- src/
|   |-- common.py              # helpers compartidos (explotar listas, ISO-3, idiomas)
|   |-- d3_treemap.py          # treemap D3 (Python -> JSON -> D3)
|   |-- data/clean_data.py     # limpieza + reglas de negocio
|   |-- analysis/              # eda_complete.py (EA1), eda_seaborn.py (EA2)
|   `-- export/                # export_powerbi.py, build_d3.py
|-- dashboard/                 # Streamlit: app.py (portada), utils.py, pages/1_Ejecutivo, 2_Analitico
|-- dash_app/app.py            # dashboard financiero en Dash
|-- d3/treemap_generos.html    # treemap D3 autónomo
|-- powerbi/                   # data/ (CSV estrella) + GUIA_POWERBI.md (+ StreamView.pbix que construyes tú)
|-- docs/                      # problema, limpieza, EDA, ética, EA2 (arquitectura, justificación, gitflow, guion)
|-- reports/, images/, notebooks/
`-- .github/pull_request_template.md
```

## Decisiones de datos relevantes (EA2)

- **Clave única `uid`**: `show_id` se repite entre películas y series (397 casos).
- **Calificación** (`calificacion`): `vote_average` solo con ≥ 10 votos (con menos es ruido). Promedio EA2: **6,63**; el 5,69 de EA1 incluía 4.560 títulos con 0 votos como «nota 0».
- **Popularidad por percentil dentro del tipo** (`popularity_pct`) para comparar géneros/países sin mezclar escalas de series y películas.
- **Financiero**: solo películas con presupuesto e ingresos (3.540); ROI = ingresos / presupuesto; presupuestos < USD 10.000 excluidos de rankings.

## Limitaciones

- No existe clasificación etaria en los datos (el campo `rating` es numérico y duplica `vote_average`); el filtro aparece deshabilitado.
- El extracto tiene ≈2.000 títulos por año, por lo que la evolución temporal es plana.
- Datos financieros para el 22% de las películas y ninguna serie.
- `popularity` es un índice relativo, no reproducciones. Los resultados describen asociaciones, no causalidad.

## Ética y uso responsable

Ver [`docs/etica_privacidad.md`](docs/etica_privacidad.md). El análisis no debe automatizar decisiones de adquisición sin criterio humano.
