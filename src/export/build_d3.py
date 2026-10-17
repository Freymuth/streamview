"""
StreamView Analytics - EA2
Genera d3/treemap_generos.html: treemap D3 autónomo (se abre con doble clic; requiere internet
para cargar D3 desde jsDelivr). Python prepara los datos y D3 los dibuja.

Ejecutar desde la raíz: python src/export/build_d3.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.getcwd())
from src.common import explotar, separar  # noqa: E402
from src.d3_treemap import construir_html_treemap  # noqa: E402


def main():
    cat = pd.read_csv("data/processed/catalogo_limpio.csv")
    cat["lista_generos"] = cat["genres"].map(separar)
    g = explotar(cat, "lista_generos", "genero")
    tabla = g.groupby("genero").agg(titulos=("uid", "count"), calificacion=("calificacion", "mean"),
                                    popularidad=("popularity", "mean")).reset_index()
    os.makedirs("d3", exist_ok=True)
    html = construir_html_treemap(tabla, titulo="StreamView · Géneros por volumen (tamaño = títulos)", ancho=1000, alto=520)
    with open("d3/treemap_generos.html", "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"✅ d3/treemap_generos.html ({len(tabla)} géneros)")


if __name__ == "__main__":
    main()
