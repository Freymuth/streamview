"""
StreamView Analytics - EA2
Gráficos estáticos con Seaborn para la documentación (docs/) y la presentación.

  - images/eda/10_correlaciones.png        mapa de calor de correlaciones (Spearman)
  - images/eda/11_distribucion_calificacion.png   distribución de calificación por tipo

Ejecutar desde la raíz: python src/analysis/eda_seaborn.py
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

IMG_DIR = "images/eda/"
COLORES = {"Movie": "#2563EB", "TV Show": "#F97316"}


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    cat = pd.read_csv("data/processed/catalogo_limpio.csv")
    fin = pd.read_csv("data/processed/catalogo_financiero.csv")
    sns.set_theme(style="whitegrid", font_scale=0.95)

    # 1) Correlaciones (películas con datos financieros completos)
    num = fin[["popularity", "calificacion", "vote_count", "budget", "revenue"]].copy()
    num["vote_count"] = np.log10(num["vote_count"] + 1)
    num["budget"] = np.log10(num["budget"])
    num["revenue"] = np.log10(num["revenue"])
    num.columns = ["Popularidad", "Calificación", "log Votos", "log Presupuesto", "log Ingresos"]
    corr = num.corr(method="spearman")
    fig, ax = plt.subplots(figsize=(6.5, 5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", vmin=0, vmax=1, square=True, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Correlación de Spearman (películas con datos financieros)")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}10_correlaciones.png", dpi=150)
    plt.close(fig)

    # 2) Distribución de calificación por tipo (solo títulos con votos)
    con_nota = cat.dropna(subset=["calificacion"])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.kdeplot(data=con_nota, x="calificacion", hue="type", palette=COLORES, fill=True, common_norm=False, alpha=0.35, ax=ax)
    ax.set_xlabel("Calificación (0-10)")
    ax.set_ylabel("Densidad")
    ax.set_title("Distribución de la calificación por tipo (títulos con votos)")
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}11_distribucion_calificacion.png", dpi=150)
    plt.close(fig)
    print(f"  -> {IMG_DIR}10_correlaciones.png\n  -> {IMG_DIR}11_distribucion_calificacion.png")


if __name__ == "__main__":
    main()
