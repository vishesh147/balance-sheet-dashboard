from __future__ import annotations
from turtle import width
from dash import Dash, dash_table, dcc, html, Input, Output
from numpy import pad, sort
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from BalanceSheetScraper import BalanceSheet as bs
from BalanceSheetScraper import *
   
   
app = Dash(__name__)

figbar = px.line(data_frame=bs, x='Year', y=bs['Cash & Equivalents'])
figbar.update_layout(autosize=True,
    margin=dict(
    l=0,
    r=0,
    b=0,
    t=0,
    pad=0
    ),
)

app.layout = html.Div([
    dcc.Graph(figure=figbar, config={'displaylogo': False})
])

if __name__ == '__main__':
    app.run_server(debug=True)