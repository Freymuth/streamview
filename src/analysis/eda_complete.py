"""
StreamView Analytics - EA1
Análisis exploratorio completo: genera las 8 visualizaciones requeridas por
el caso (sección "Visualización de gráficos" de los requerimientos) y sus
reportes de respaldo en CSV.

Cada gráfico se eligió según el tipo de variable y el propósito analítico:
  - Proporciones de un total (tipo, país, idioma, género)  -> torta / barras horizontales
  - Comparar distribuciones entre 2 grupos (Movie/TV Show)  -> boxplot
  - Relación entre 2 variables numéricas                    -> dispersión (scatter)
  - Evolución en el tiempo                                  -> líneas
  - Ranking Top-N                                           -> barras horizontales ordenadas

Ejecutar desde la raíz del proyecto: python src/analysis/eda_complete.py
Genera imágenes en images/eda/ y tablas de respaldo en reports/eda/
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

PROCESSED_DIR = "data/processed/"
IMG_DIR = "images/eda/"
REPORT_DIR = "reports/eda/"

COLOR_MOVIE = "#2563EB"
COLOR_TV = "#F97316"

plt.rcParams["figure.dpi"] = 150
plt.rcParams["font.size"] = 10


def guardar_figura(fig, nombre):
    fig.tight_layout()
    fig.savefig(f"{IMG_DIR}{nombre}.png", bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {IMG_DIR}{nombre}.png")


def explotar(df, columna, nueva):
    out = df.assign(**{nueva: df[columna].str.split(", ")}).explode(nueva)
    return out[out[nueva] != "Desconocido"]


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    catalogo = pd.read_csv(f"{PROCESSED_DIR}catalogo_limpio.csv")
    financiero = pd.read_csv(f"{PROCESSED_DIR}catalogo_financiero.csv")

    # =======================================================================
    # 1. CARACTERIZACIÓN Y ESTRUCTURA DEL CATÁLOGO
    # =======================================================================
    print("1) Caracterización y estructura del catálogo")

    # 1a. Distribución de películas vs series -> torta (proporción de un total)
    conteo_tipo = catalogo["type"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(conteo_tipo.values, labels=conteo_tipo.index, autopct="%1.1f%%",
           colors=[COLOR_MOVIE, COLOR_TV], startangle=90)
    ax.set_title("Distribución del catálogo: películas vs series")
    guardar_figura(fig, "01_distribucion_tipo")
    conteo_tipo.to_csv(f"{REPORT_DIR}distribucion_tipo.csv", header=["cantidad"])

    # 1b. Géneros predominantes -> barras horizontales (ranking Top-N)
    generos = explotar(catalogo, "genres", "genero")
    top_generos = generos["genero"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_generos.sort_values().index, top_generos.sort_values().values, color="#3B82F6")
    ax.set_xlabel("Cantidad de títulos")
    ax.set_title("Top 10 géneros predominantes")
    guardar_figura(fig, "02_generos_predominantes")
    top_generos.to_csv(f"{REPORT_DIR}genres.csv", header=["cantidad"])

    # 1c. Análisis geográfico e idiomas -> barras horizontales
    paises = explotar(catalogo, "country", "pais")
    top_paises = paises["pais"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_paises.sort_values().index, top_paises.sort_values().values, color="#F97316")
    ax.set_xlabel("Cantidad de títulos")
    ax.set_title("Top 10 países de producción")
    guardar_figura(fig, "03_paises")
    top_paises.to_csv(f"{REPORT_DIR}paises.csv", header=["cantidad"])

    top_idiomas = catalogo["language"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_idiomas.sort_values().index, top_idiomas.sort_values().values, color="#10B981")
    ax.set_xlabel("Cantidad de títulos")
    ax.set_title("Top 10 idiomas del catálogo")
    guardar_figura(fig, "04_idiomas")
    top_idiomas.to_csv(f"{REPORT_DIR}idiomas.csv", header=["cantidad"])

    # =======================================================================
    # 2. POPULARIDAD Y VALORACIÓN
    # =======================================================================
    print("2) Popularidad y valoración")

    # 2a. Comparativa de popularidad -> boxplot (comparar distribución entre
    # dos grupos, más honesto que comparar solo promedios)
    fig, ax = plt.subplots(figsize=(6, 5))
    data_box = [catalogo[catalogo["type"] == t]["popularity_norm"].dropna() for t in ["Movie", "TV Show"]]
    bp = ax.boxplot(data_box, tick_labels=["Movie", "TV Show"], patch_artist=True, showfliers=False)
    for patch, color in zip(bp["boxes"], [COLOR_MOVIE, COLOR_TV]):
        patch.set_facecolor(color)
    ax.set_ylabel("Popularidad normalizada (0-1)")
    ax.set_title("Comparativa de popularidad normalizada")
    guardar_figura(fig, "05_comparativa_popularidad")

    # 2b. Relación entre popularidad y calificación -> dispersión (scatter)
    muestra = catalogo.sample(min(3000, len(catalogo)), random_state=42)
    fig, ax = plt.subplots(figsize=(7, 5))
    for tipo, color in [("Movie", COLOR_MOVIE), ("TV Show", COLOR_TV)]:
        sub = muestra[muestra["type"] == tipo]
        ax.scatter(sub["popularity"], sub["vote_average"], alpha=0.4, s=10, color=color, label=tipo)
    ax.set_xscale("log")
    ax.set_xlabel("Popularidad (escala log)")
    ax.set_ylabel("Calificación promedio")
    ax.set_title("Popularidad vs. calificación de la audiencia")
    ax.legend()
    guardar_figura(fig, "06_popularidad_vs_calificacion")

    correlacion = catalogo[["popularity", "vote_average"]].corr().iloc[0, 1]
    pd.DataFrame({"correlacion_popularidad_calificacion": [round(correlacion, 4)]}).to_csv(
        f"{REPORT_DIR}correlacion_popularidad_calificacion.csv", index=False
    )

    # =======================================================================
    # 3. ANÁLISIS TEMPORAL
    # =======================================================================
    print("3) Análisis temporal")

    # Evolución histórica -> líneas (variable temporal continua)
    evolucion = catalogo.groupby(["release_year", "type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(evolucion.index, evolucion["Movie"], marker="o", color=COLOR_MOVIE, label="Movie", markersize=3)
    ax.plot(evolucion.index, evolucion["TV Show"], marker="o", color=COLOR_TV, label="TV Show", markersize=3)
    ax.set_xlabel("Año de estreno")
    ax.set_ylabel("Cantidad de títulos")
    ax.set_title("Evolución histórica de estrenos por año")
    ax.legend()
    guardar_figura(fig, "07_evolucion_historica")
    evolucion.to_csv(f"{REPORT_DIR}evolucion_historica.csv")

    # =======================================================================
    # 4. ANÁLISIS FINANCIERO (solo películas con budget/revenue conocidos)
    # =======================================================================
    print("4) Análisis financiero")

    # 4a. Presupuesto vs ingresos -> dispersión (relación entre 2 variables)
    fig, ax = plt.subplots(figsize=(7, 6))
    sc = ax.scatter(financiero["budget"], financiero["revenue"], c=financiero["vote_average"],
                     cmap="viridis", alpha=0.6, s=15)
    ax.set_xscale("log")
    ax.set_yscale("log")
    max_val = max(financiero["budget"].max(), financiero["revenue"].max())
    ax.plot([1, max_val], [1, max_val], "r--", linewidth=1, label="Ingresos = Presupuesto")
    ax.set_xlabel("Presupuesto (USD, escala log)")
    ax.set_ylabel("Ingresos (USD, escala log)")
    ax.set_title("Presupuesto vs. ingresos")
    plt.colorbar(sc, label="Calificación")
    ax.legend()
    guardar_figura(fig, "08_presupuesto_vs_ingresos")

    # 4b. Retorno de inversión -> barras horizontales (ranking Top-N),
    # excluyendo presupuestos irrealmente bajos que distorsionan el ranking.
    fin_validos = financiero[financiero["budget"] >= 10_000]
    top_roi = fin_validos.sort_values("roi", ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top_roi.sort_values("roi")["title"], top_roi.sort_values("roi")["roi"], color="#0D9488")
    ax.set_xlabel("ROI (veces el presupuesto en ingresos)")
    ax.set_title("Top 15 títulos con mayor ROI\n(excluye presupuestos menores a $10.000)")
    guardar_figura(fig, "09_top_roi")
    top_roi[["title", "budget", "revenue", "roi"]].to_csv(f"{REPORT_DIR}top_roi.csv", index=False)

    print(f"\n✅ Gráficos guardados en {IMG_DIR}")
    print(f"✅ Reportes guardados en {REPORT_DIR}")


if __name__ == "__main__":
    main()
