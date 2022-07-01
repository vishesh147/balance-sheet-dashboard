from __future__ import annotations
from turtle import width
from dash import Dash, dash_table, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from BalanceSheetScraper import BalanceSheet as bs
from BalanceSheetScraper import *

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            bs.columns.to_list(),
            'Year',
            id='line-data',
        )
    ]),
    dcc.Graph(id='linechart'),
])


@app.callback(
    Output('linechart', 'figure'),
    Input('line-data', 'value'))
def update_graph(data):
    fig = px.line(data_frame=bs, x='Year', y=data, markers=True)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    bs.columns.to_list(),
                    'Year',
                    id='line-data',
                )
            ], style={'width':'50%', 'padding-left':'50px', 'padding-bottom':'10px'}),
        dcc.Graph(id='linechart', style={'height':'40vh'})
        ], style={'width':'50%', 'padding-right':'50px'}),

        html.Div([
            dcc.Dropdown(
                options=[
                    {'label': 'Debt-to-Equity Ratio', 'value': "DE Ratio,Total Long Term Debt,Total Equity"},
                    {'label': 'Debt-to-Assets Ratio', 'value': "DA Ratio,Total Long Term Debt,Total Assets"},
                # {'label': 'Debt-to-Capital Ratio', 'value': "DC Ratio,Total Long Term Debt,Total Equity"},
                ],
                value="DE Ratio,Total Long Term Debt,Total Equity",
                id='leverage-ratio',
            )
        ], style={'width':'50%'}),
        html.Div([
            dcc.Graph(id='leverage-ratio-pie', config={'displaylogo': False}, style={'width':'50%'}),
            dcc.Graph(id='leverage-ratio-line', config={'displaylogo': False}, style={'width':'50%', 'height':'40vh'}),
        ], style={'display':'flex'}),
    ], style={'display':'flex'})
