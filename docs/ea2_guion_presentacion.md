# EA2 · Guion de presentación (≈10 minutos)

**Foco pedido:** explicar la **arquitectura** y las **herramientas** usadas.

| # | Diapositiva | Qué decir | Tiempo |
|---|---|---|---|
| 1 | Contexto | StreamView, problema (reportes dispersos), audiencias elegidas: Directorio/Gerencia General y Contenidos/Adquisición. | 1' |
| 2 | Datos | 2 datasets oficiales → 31.991 títulos; decisiones de calidad: `uid`, calificación ≥10 votos, percentil de popularidad. | 1,5' |
| 3 | **Arquitectura** | Mostrar el diagrama de `docs/ea2_arquitectura.md`: raw → clean_data → processed → (Streamlit · Dash · D3 · Power BI). Una sola fuente, un solo cálculo de cada KPI. | 2' |
| 4 | **Herramientas** | Tabla «Rol de cada herramienta»: por qué Streamlit, Plotly, Dash, D3, Seaborn y Power BI. | 1,5' |
| 5 | Demo Dashboard Ejecutivo | KPIs → evolución → mapa → filtros. Responder: ¿cómo evolucionó?, ¿qué predomina? (y advertir la distribución uniforme por año). | 1,5' |
| 6 | Demo Dashboard Analítico | Dispersión + correlación por tipo, treemap D3, mapa con mínimo de títulos, bloque financiero y nota visible. | 2' |
| 7 | Conclusiones | Pestaña «Conclusiones»: géneros a priorizar, países oportunidad, éxitos con presupuesto reducido, relación popularidad–calificación. | 1' |
| 8 | Gestión y limitaciones | Gitflow (ramas/PR), limitaciones: sin clasificación etaria, datos financieros 22%, asociación ≠ causalidad. | 1' |

**Preguntas probables:** ¿por qué la calificación promedio cambió de 5,69 a 6,63? (regla ≥10 votos) · ¿por qué Spearman y por tipo? (escalas distintas, outliers) · ¿por qué no hay filtro de clasificación etaria? (no existe en los datos) · ¿qué aporta cada herramienta? (tabla de roles).
