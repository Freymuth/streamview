"""
StreamView Analytics - EA2
Utilidades compartidas por el pipeline, los dashboards (Streamlit/Dash),
la exportación a Power BI y la visualización D3.

Una sola definición de cada helper => una sola versión de cada indicador
(problema 1 del caso: "múltiples versiones de un mismo indicador").
"""

from functools import lru_cache

import pandas as pd
import pycountry

DESCONOCIDOS = {"Desconocido", "Unknown", ""}

# Países que pycountry no resuelve por nombre (nombres estilo TMDB).
OVERRIDES_ISO3 = {
    "Russia": "RUS",
    "Turkey": "TUR",
    "Macedonia": "MKD",
    "Kosovo": "XKX",
    "Cote D'Ivoire": "CIV",
    "Palestinian Territory": "PSE",
    "Faeroe Islands": "FRO",
    "Guadaloupe": "GLP",
    "St. Kitts and Nevis": "KNA",
    "St. Lucia": "LCA",
    "St. Pierre and Miquelon": "SPM",
    "US Virgin Islands": "VIR",
    "Netherlands Antilles": "ANT",
}

# TMDB usa algunos códigos que no son ISO 639-1.
OVERRIDES_IDIOMA = {"cn": "Cantonese", "xx": "Sin idioma"}


@lru_cache(maxsize=None)
def pais_a_iso3(nombre):
    """Nombre de país (TMDB) -> código ISO-3 para mapas coropléticos."""
    if nombre in OVERRIDES_ISO3:
        return OVERRIDES_ISO3[nombre]
    try:
        return pycountry.countries.lookup(nombre).alpha_3
    except LookupError:
        return None


@lru_cache(maxsize=None)
def idioma_nombre(codigo):
    """Código de idioma (en, ko, ...) -> nombre legible."""
    if codigo in OVERRIDES_IDIOMA:
        return OVERRIDES_IDIOMA[codigo]
    lang = pycountry.languages.get(alpha_2=codigo) if isinstance(codigo, str) else None
    if lang is None:
        return str(codigo)
    nombre = getattr(lang, "common_name", None) or lang.name
    return nombre.split(" (")[0]


def separar(texto):
    """'A, B, C' -> ['A','B','C'] sin valores desconocidos."""
    if not isinstance(texto, str):
        return []
    return [x.strip() for x in texto.split(", ") if x.strip() not in DESCONOCIDOS]


def explotar(df, columna_lista, nueva):
    """Una fila por elemento de una columna que contiene listas."""
    out = df.drop(columns=[nueva], errors="ignore").explode(columna_lista)
    out = out.rename(columns={columna_lista: nueva})
    return out.dropna(subset=[nueva])
