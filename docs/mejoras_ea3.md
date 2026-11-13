# Mejoras implementadas en EA3 (antes → después)

Se revisan en la ejecución posterior a la presentación. Para verlas:

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

| ID | Mejora | Dónde verla | Antes | Después |
|---|---|---|---|---|
| M1 | Página **Calidad y EDA** (pasos 4-7 de la guía 3.1.1) | menú lateral → «Calidad y EDA» · `dashboard/pages/3_Calidad_y_EDA.py` | No había forma de ver datos faltantes ni outliers | 4 pestañas: calidad, distribuciones (histograma + boxplot), correlaciones (Spearman) y anomalías de ROI (regla IQR) |
| M2 | **Cifras coherentes** en todo el proyecto | `src/analysis/eda_complete.py`, `docs/resultados_eda.md`, `reports/eda/roi_definiciones.csv` | Nota 5,69 / corr. 0,03 / «crecimiento sostenido» | Nota 6,63 / Spearman 0,23 y 0,17 / serie plana explicada / 3 definiciones de ROI |
| M3 | **Lectura rápida** (storytelling) | Dashboard Ejecutivo, bajo los KPI | Solo KPI y gráficos | Frase dinámica con tipo, género y país líderes y nota por tipo |
| M4 | **Exportar CSV** de lo filtrado | Final del Dashboard Ejecutivo | Sin exportación | Botón «Descargar los títulos filtrados» |
| M5 | **Reproducibilidad** | `data/processed/`, `notebooks/01_analisis_completo.ipynb`, `README.md` | Procesados ignorados, solo `.py` | Se ejecuta sin pasos previos; notebook; README actualizado |
| M6 | **Eje Y desde 0** en el gráfico de evolución histórica | `images/eda/07_evolucion_historica.png` | El eje truncado hacía parecer una caída fuerte en 2025 (991 vs. 1.000 series) | Eje desde 0: se ve la serie plana tal como es |

## Correcciones al informe y a la presentación tras revisar la pauta EP6
| Cambio | Dónde |
|---|---|
| Sección de **impacto esperado** en la toma de decisiones (sin cifras inventadas; con cómo medirlo) | Informe 10.3; presentación diap. 10 |
| **Sesgos, riesgos y mitigación** (cobertura financiera, selección en la nota, composición por tipo, origen, muestreo, atípicos, interpretación) | Informe 9.3; presentación diap. 8 |
| **Mejoras priorizadas** por impacto y esfuerzo | Informe 9.5; presentación diap. 9 |
| Fortalezas con evidencia verificable | Informe 9.1; presentación diap. 7 |
| Atributos visuales y criterios de representación | Informe 6.1; presentación diap. 4 |
| Presentación rehecha con los apartados de la pauta (11 diapositivas para 10 minutos) | `docs/StreamView_Presentacion_EA3.pptx` |
| Fuentes de datos y alcance declarado (sin usuarios, reproducciones ni dispositivos) | Informe sección 4; presentación diap. 2 |
| **Corrección de contenido:** la ventaja de Japón y Corea del Sur se compara dentro de cada tipo, porque la nota agregada por país mezcla películas y series | Informe R2 y 9.3; presentación; `conclusiones_recomendaciones.md` |
| Se quitó una nota interna sobre el documento 3.3.1 que había quedado dentro del informe | Informe sección 9 |
