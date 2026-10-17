"""
StreamView Analytics - EA1
Notebook (versión script) que documenta el flujo completo paso a paso:
limpieza -> reglas de negocio -> análisis exploratorio -> gráficos.

Ejecutar desde la raíz del proyecto: python notebooks/01_analisis_completo.py
"""

import sys

sys.path.append(".")
from src.data.clean_data import main as limpiar_datos
from src.analysis.eda_complete import main as generar_eda
from src.analysis.eda_seaborn import main as generar_seaborn
from src.export.build_d3 import main as generar_d3
from src.export.export_powerbi import main as exportar_powerbi

print("=" * 60)
print("PASO 1: Limpieza y preparación de datos + reglas de negocio")
print("=" * 60)
limpiar_datos()

print("\n" + "=" * 60)
print("PASO 2: Análisis exploratorio y generación de gráficos")
print("=" * 60)
generar_eda()

print("\n" + "=" * 60)
print("PASO 3 (EA2): Seaborn, treemap D3 y exportación para Power BI")
print("=" * 60)
generar_seaborn()
generar_d3()
exportar_powerbi()

print("\n" + "=" * 60)
print("Flujo completo. Revisa docs/resultados_eda.md para el resumen")
print("narrativo, o corre `streamlit run dashboard/app.py` para el")
print("dashboard interactivo.")
print("=" * 60)
