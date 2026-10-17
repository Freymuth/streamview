# Gestión del repositorio · Gitflow (EA2)

## Ramas

| Rama | Uso |
|---|---|
| `main` | Solo versiones entregables (se actualiza con un PR desde `develop` + tag). |
| `develop` | Integración continua del trabajo. |
| `feature/<nombre>` | Una por funcionalidad; nace de `develop` y vuelve por Pull Request. |
| `hotfix/<nombre>` | Corrección urgente sobre `main`. |

## Convención de commits
`tipo(alcance): descripción` — tipos: `feat`, `fix`, `docs`, `refactor`, `chore`.
Ejemplo: `feat(ejecutivo): agrega mapa coroplético de producciones`

## Plan sugerido (qué archivos van en cada rama)

| # | Rama | Archivos | Requerimiento EA2 |
|---|---|---|---|
| 1 | `feature/data-uid-calificacion` | `src/common.py`, `src/data/clean_data.py` | Calidad de datos, uid, calificación |
| 2 | `feature/dashboard-base` | `dashboard/__init__.py`, `dashboard/utils.py`, `dashboard/app.py` | Filtros, formato, portada |
| 3 | `feature/dashboard-ejecutivo` | `dashboard/pages/1_Ejecutivo.py` | Req. 2 |
| 4 | `feature/dashboard-analitico` | `dashboard/pages/2_Analitico.py` | Req. 3 |
| 5 | `feature/d3-treemap` | `src/d3_treemap.py`, `src/export/build_d3.py`, `d3/` | D3 |
| 6 | `feature/dash-financiero` | `dash_app/app.py` | Dash |
| 7 | `feature/seaborn-eda` | `src/analysis/eda_seaborn.py`, `images/eda/10_*`, `11_*` | Seaborn |
| 8 | `feature/powerbi` | `src/export/export_powerbi.py`, `powerbi/` | Power BI |
| 9 | `docs/ea2` | `docs/`, `README.md`, `.github/` | Req. 6 y 7 |

## Comandos

```bash
# una sola vez
git checkout main && git pull
git checkout -b develop && git push -u origin develop

# por cada feature (ejemplo: ejecutivo)
git checkout develop && git pull
git checkout -b feature/dashboard-ejecutivo
git add dashboard/pages/1_Ejecutivo.py
git commit -m "feat(ejecutivo): dashboard ejecutivo con KPIs, filtros y mapa"
git push -u origin feature/dashboard-ejecutivo
# abrir Pull Request en GitHub: base = develop  (usa la plantilla .github/pull_request_template.md)
# tras aprobar y hacer merge:
git checkout develop && git pull

# entrega: PR de develop a main y etiqueta
git checkout main && git merge --no-ff develop
git tag -a v2.0-ea2 -m "Entrega EA2"
git push origin main --tags
```

> **Importante para la evaluación:** el historial real (ramas, commits y PRs) es la evidencia de Gitflow.
> Crea las ramas y PRs en GitHub **antes** de entregar; compartir solo un zip sin historial no demuestra el flujo.
