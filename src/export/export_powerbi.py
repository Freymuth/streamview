"""
StreamView Analytics - EA2
Exporta el modelo en estrella para Power BI a powerbi/data/.

Tablas (relaciones por la columna uid):
  fact_catalogo      1 fila por título (tabla central)
  fact_financiero    1 fila por película con budget y revenue conocidos
  bridge_genero      uid, genero          (un título -> varios géneros)
  bridge_pais        uid, pais, iso3      (un título -> varios países)
  bridge_director    uid, director
  bridge_actor       uid, actor
  dim_calendario     anio

Ejecutar desde la raíz: python src/export/export_powerbi.py
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.getcwd())
from src.common import explotar, pais_a_iso3, separar  # noqa: E402

OUT = "powerbi/data/"


def main():
    os.makedirs(OUT, exist_ok=True)
    cat = pd.read_csv("data/processed/catalogo_limpio.csv", parse_dates=["date_added"])
    fin = pd.read_csv("data/processed/catalogo_financiero.csv")
    for col, nueva in [("genres", "lista_generos"), ("country", "lista_paises"),
                       ("director", "lista_directores"), ("cast", "lista_actores")]:
        cat[nueva] = cat[col].map(separar)

    fact = cat[["uid", "show_id", "type", "title", "release_year", "anio_incorporacion", "idioma_nombre",
                "popularity", "popularity_pct", "vote_count", "vote_average", "calificacion"]].rename(columns={
        "type": "tipo", "title": "titulo", "release_year": "anio_estreno", "idioma_nombre": "idioma",
        "popularity": "popularidad", "popularity_pct": "popularidad_percentil", "vote_count": "votos", "vote_average": "vote_average_original"})
    fact["tipo"] = fact["tipo"].map({"Movie": "Película", "TV Show": "Serie"})
    fact.to_csv(OUT + "fact_catalogo.csv", index=False, encoding="utf-8-sig")

    fin[["uid", "title", "budget", "revenue", "roi", "ganancia", "presupuesto_realista"]].rename(
        columns={"title": "titulo", "budget": "presupuesto", "revenue": "ingresos", "ganancia": "ganancia"}
    ).to_csv(OUT + "fact_financiero.csv", index=False, encoding="utf-8-sig")

    explotar(cat[["uid", "lista_generos"]], "lista_generos", "genero").to_csv(OUT + "bridge_genero.csv", index=False, encoding="utf-8-sig")
    p = explotar(cat[["uid", "lista_paises"]], "lista_paises", "pais")
    p["iso3"] = p["pais"].map(pais_a_iso3)
    p.to_csv(OUT + "bridge_pais.csv", index=False, encoding="utf-8-sig")
    explotar(cat[["uid", "lista_directores"]], "lista_directores", "director").to_csv(OUT + "bridge_director.csv", index=False, encoding="utf-8-sig")
    explotar(cat[["uid", "lista_actores"]], "lista_actores", "actor").to_csv(OUT + "bridge_actor.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame({"anio": range(int(cat["release_year"].min()), int(cat["release_year"].max()) + 1)}).to_csv(
        OUT + "dim_calendario.csv", index=False)

    for f in sorted(os.listdir(OUT)):
        print(f"✅ {OUT}{f}  ({sum(1 for _ in open(OUT + f, encoding='utf-8-sig')) - 1:,} filas)")


if __name__ == "__main__":
    main()
