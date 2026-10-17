"""
StreamView Analytics - EA2
Dashboard FINANCIERO de películas en Dash (Plotly). Complementa a Streamlit:
mismo dato procesado, otro framework (callbacks explícitos).

Ejecutar desde la raíz del proyecto:  python dash_app/app.py   ->  http://127.0.0.1:8050
Reglas del caso: solo películas con presupuesto e ingresos informados; ROI = ingresos / presupuesto.
"""

import os
import sys

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

sys.path.insert(0, os.getcwd())
from src.common import separar  # noqa: E402

RUTA = "data/processed/catalogo_financiero.csv"
if not os.path.exists(RUTA):
    from src.data.clean_data import main as correr_pipeline

    correr_pipeline()

fin = pd.read_csv(RUTA)
fin["lista_generos"] = fin["genres"].map(separar)
GENEROS = sorted({g for l in fin["lista_generos"] for g in l})
A_MIN, A_MAX = int(fin["release_year"].min()), int(fin["release_year"].max())
AZUL = "#2563EB"


def usd_m(x):
    return f"USD {round(x / 1e6):,} M".replace(",", ".")


def tarjeta(titulo, valor):
    return html.Div(
        [html.Div(titulo, style={"fontSize": 12, "color": "#6B7280"}),
         html.Div(valor, style={"fontSize": 24, "fontWeight": 700})],
        style={"flex": 1, "padding": "12px 16px", "border": "1px solid #E5E7EB", "borderRadius": 8},
    )


app = Dash(__name__, title="StreamView · Financiero")
app.layout = html.Div(
    style={"fontFamily": "Segoe UI, system-ui, sans-serif", "maxWidth": 1200, "margin": "0 auto", "padding": 16},
    children=[
        html.H2("💰 Dashboard financiero de películas (Dash)"),
        html.Div(
            "Solo se incluyen películas con presupuesto e ingresos informados "
            f"({len(fin):,} de 16.000 películas).".replace(",", "."),
            style={"background": "#EFF6FF", "padding": 10, "borderRadius": 6, "marginBottom": 12},
        ),
        html.Div(
            style={"display": "flex", "gap": 24, "marginBottom": 12},
            children=[
                html.Div([html.Label("Género"), dcc.Dropdown(GENEROS, id="f-genero", multi=True, placeholder="Todos")],
                         style={"flex": 1}),
                html.Div([html.Label("Años de estreno"),
                          dcc.RangeSlider(A_MIN, A_MAX, 1, value=[A_MIN, A_MAX], id="f-anios",
                                          marks={a: str(a) for a in range(A_MIN, A_MAX + 1, 3)})], style={"flex": 1}),
            ],
        ),
        html.Div(id="kpis", style={"display": "flex", "gap": 12, "marginBottom": 12}),
        html.Div(style={"display": "flex", "gap": 12},
                 children=[dcc.Graph(id="g-disp", style={"flex": 1}), dcc.Graph(id="g-top", style={"flex": 1})]),
    ],
)


def filtrar(generos, anios):
    df = fin[fin["release_year"].between(*anios)]
    if generos:
        sel = set(generos)
        df = df[df["lista_generos"].map(lambda l: bool(sel & set(l)))]
    return df


@app.callback(
    Output("kpis", "children"), Output("g-disp", "figure"), Output("g-top", "figure"),
    Input("f-genero", "value"), Input("f-anios", "value"),
)
def actualizar(generos, anios):
    df = filtrar(generos, anios)
    if df.empty:
        vacio = go.Figure().update_layout(template="plotly_white", title="Sin datos con estos filtros")
        return [tarjeta("Películas", "0")], vacio, vacio
    kpis = [
        tarjeta("Películas analizadas", f"{len(df):,}".replace(",", ".")),
        tarjeta("Presupuesto promedio", usd_m(df["budget"].mean())),
        tarjeta("Total presupuesto", usd_m(df["budget"].sum())),
        tarjeta("Total ingresos", usd_m(df["revenue"].sum())),
        tarjeta("ROI aproximado", f"{df['revenue'].sum() / df['budget'].sum():.2f}x".replace(".", ",")),
    ]
    disp = px.scatter(df, x="budget", y="revenue", log_x=True, log_y=True, hover_name="title", opacity=0.6,
                      color_discrete_sequence=[AZUL],
                      labels={"budget": "Presupuesto (USD, log)", "revenue": "Ingresos (USD, log)"})
    lo, hi = df["budget"].min(), max(df["budget"].max(), df["revenue"].max())
    disp.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines", name="ROI = 1",
                              line=dict(color="#DC2626", dash="dash")))
    disp.update_layout(template="plotly_white", title="Presupuesto vs. ingresos", showlegend=False)
    top = df.sort_values("revenue", ascending=False).head(10).sort_values("revenue")
    top["m"] = top["revenue"] / 1e6
    barras = px.bar(top, x="m", y="title", orientation="h", color_discrete_sequence=[AZUL],
                    labels={"m": "Ingresos (millones de USD)", "title": ""})
    barras.update_layout(template="plotly_white", title="Top 10 películas por ingresos")
    return kpis, disp, barras


if __name__ == "__main__":
    app.run(debug=False)
