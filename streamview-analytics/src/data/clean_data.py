"""
StreamView Analytics - EA1
Limpieza, unificación y reglas de negocio sobre los datasets oficiales del caso.

Ejecutar desde la raíz del proyecto: python src/data/clean_data.py
Genera:
  - data/processed/catalogo_limpio.csv
  - data/processed/catalogo_financiero.csv
  - reports/data_quality/cleaning_summary.csv
"""

import os
import pandas as pd

RAW_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"
REPORT_DIR = "reports/data_quality/"


def cargar_datos_crudos(path_prefix=RAW_DIR):
    tv = pd.read_csv(f"{path_prefix}netflix_tv_shows_detailed_up_to_2025.csv")
    mv = pd.read_csv(f"{path_prefix}netflix_movies_detailed_up_to_2025.csv")
    return tv, mv


def limpiar_datasets(tv, mv, resumen):
    """Codificación y preparación de datos. Registra cada decisión en `resumen`."""
    tv, mv = tv.copy(), mv.copy()

    resumen.append(("rating (TV)", "eliminada", "idéntica a vote_average en 100% de los casos"))
    resumen.append(("rating (Movies)", "eliminada", "idéntica a vote_average en 100% de los casos"))
    tv = tv.drop(columns=["rating"], errors="ignore")
    mv = mv.drop(columns=["rating"], errors="ignore")

    resumen.append(("duration (Movies)", "eliminada", "100% de valores nulos"))
    mv = mv.drop(columns=["duration"], errors="ignore")
    tv = tv.drop(columns=["duration"], errors="ignore")

    tv["date_added"] = pd.to_datetime(tv["date_added"], errors="coerce")
    mv["date_added"] = pd.to_datetime(mv["date_added"], errors="coerce")
    resumen.append(("date_added", "convertida", "texto -> datetime"))

    dup_tv = tv["show_id"].duplicated().sum()
    dup_mv = mv["show_id"].duplicated().sum()
    tv = tv.drop_duplicates(subset="show_id", keep="first")
    mv = mv.drop_duplicates(subset="show_id", keep="first")
    resumen.append(("show_id duplicados (TV)", f"{dup_tv} eliminados", "keep='first'"))
    resumen.append(("show_id duplicados (Movies)", f"{dup_mv} eliminados", "keep='first'"))

    for col in ["director", "cast", "country", "genres", "description"]:
        n_nulos_tv = tv[col].isna().sum() if col in tv.columns else 0
        n_nulos_mv = mv[col].isna().sum() if col in mv.columns else 0
        if col in tv.columns:
            tv[col] = tv[col].fillna("Desconocido")
        if col in mv.columns:
            mv[col] = mv[col].fillna("Desconocido")
        resumen.append((f"{col} (nulos)", f"TV: {n_nulos_tv} / Movies: {n_nulos_mv}", "rellenados con 'Desconocido'"))

    return tv, mv


def unificar_catalogo(tv, mv):
    tv = tv.copy()
    tv["budget"] = pd.NA
    tv["revenue"] = pd.NA
    catalogo = pd.concat([mv, tv], ignore_index=True)
    catalogo["budget"] = pd.to_numeric(catalogo["budget"], errors="coerce")
    catalogo["revenue"] = pd.to_numeric(catalogo["revenue"], errors="coerce")
    return catalogo


def aplicar_reglas_negocio(catalogo, resumen):
    catalogo = catalogo.copy()

    ceros_budget = (catalogo["budget"] == 0).sum()
    ceros_revenue = (catalogo["revenue"] == 0).sum()
    catalogo.loc[catalogo["budget"] == 0, "budget"] = pd.NA
    catalogo.loc[catalogo["revenue"] == 0, "revenue"] = pd.NA
    resumen.append(("budget/revenue == 0", f"{ceros_budget} / {ceros_revenue} -> NA", "0 significa 'dato no disponible', no costo/ingreso cero"))

    catalogo["popularity_norm"] = catalogo.groupby("type")["popularity"].transform(
        lambda x: (x - x.min()) / (x.max() - x.min())
    )
    resumen.append(("popularity_norm", "creada", "normalización 0-1 por tipo (Movie/TV Show)"))

    financiero = catalogo.dropna(subset=["budget", "revenue"]).copy()
    financiero["roi"] = financiero["revenue"] / financiero["budget"]
    financiero["ganancia"] = financiero["revenue"] - financiero["budget"]
    resumen.append(("catalogo_financiero", f"{len(financiero)} de {len(catalogo)} títulos", "filtrado: budget y revenue conocidos (regla de negocio)"))
    resumen.append(("roi", "creada", "ROI = revenue / budget (definición oficial del caso)"))

    return catalogo, financiero


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    resumen = []
    tv, mv = cargar_datos_crudos()
    print(f"TV Shows cargados: {len(tv)} filas | Movies cargadas: {len(mv)} filas")

    tv, mv = limpiar_datasets(tv, mv, resumen)
    catalogo = unificar_catalogo(tv, mv)
    catalogo, financiero = aplicar_reglas_negocio(catalogo, resumen)

    catalogo.to_csv(f"{PROCESSED_DIR}catalogo_limpio.csv", index=False)
    financiero.to_csv(f"{PROCESSED_DIR}catalogo_financiero.csv", index=False)

    pd.DataFrame(resumen, columns=["campo", "accion", "justificacion"]).to_csv(
        f"{REPORT_DIR}cleaning_summary.csv", index=False
    )

    print(f"\n✅ {PROCESSED_DIR}catalogo_limpio.csv ({len(catalogo)} filas)")
    print(f"✅ {PROCESSED_DIR}catalogo_financiero.csv ({len(financiero)} filas)")
    print(f"✅ {REPORT_DIR}cleaning_summary.csv ({len(resumen)} decisiones documentadas)")


if __name__ == "__main__":
    main()
