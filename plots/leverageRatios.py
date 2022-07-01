from __future__ import annotations
from turtle import width
from dash import Dash, dash_table, dcc, html, Input, Output
from numpy import sort
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
            options=[
                {'label': 'Debt-to-Equity Ratio', 'value': "DE Ratio,Total Long Term Debt,Total Equity"},
                {'label': 'Debt-to-Assets Ratio', 'value': "DA Ratio,Total Long Term Debt,Total Assets"},
               # {'label': 'Debt-to-Capital Ratio', 'value': "DC Ratio,Total Long Term Debt,Total Equity"},
            ],
            value="DE Ratio,Total Long Term Debt,Total Equity",
            id='ratio',
        )
    ], style={'width':'50%'}),
    html.Div([
        dcc.Graph(id='ratio-pie', config={'displaylogo': False}, style={'width':'50%'}),
        dcc.Graph(id='ratio-line', config={'displaylogo': False}, style={'width':'50%', 'height':'40vh'}),
    ], style={'display':'flex'}),
], style={'width':'50%'}) 


@app.callback(
    Output('ratio-line', 'figure'),
    Input('ratio', 'value'))
def update_graph(ratio):
    data = list(str(ratio).split(','))
    fig = px.area(
        data_frame=bs,
        text=["<b>%.2f<b>" %s for s in bs[data[0]].to_list()],
        x="Year", 
        y=data[0],
        custom_data = [bs[data[1]].to_list(), bs[data[2]].to_list()],
        range_y=[0, max(bs[data[0]].to_list()) + 0.5], 
        range_x=[-.4, 3.5],
        markers=True,
    )
    fig.update_traces(
        textposition="top center", 
        textfont_size=14,
        hovertemplate= "<b>%{x}</b><br><br><b>"+data[1]+":</b> %{customdata[0]}<br><b>"+data[2]+":</b> %{customdata[1]}"
    )
    fig.update_xaxes(showgrid=False, tickfont=dict(size=12), fixedrange=True)
    fig.update_yaxes(showticklabels=False, showgrid=False, fixedrange=True, zeroline=False)
    fig.update_layout(autosize=False,
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0
        ),
    )
    return fig

@app.callback(
    Output('ratio-pie', 'figure'),
    Input('ratio', 'value'))
def update_graph(ratio):
    data = list(str(ratio).split(','))
    fig = px.pie(
        data_frame=bs,
        names=[data[1], data[2]],
        values=[bs[data[1]].to_list()[-1], bs[data[2]].to_list()[-1]], 
        labels=[data[1], data[2]],
        hole=.6,
        color=[data[1], data[2]],
    )
    fig.add_annotation(x=0.5, y=0.5,
        text="<b>%.2f</b>" % bs[data[0]].to_list()[-1],
        font_size=30,
        showarrow=False,
    )
    fig.update_traces(textinfo='none', hovertemplate= "<b>%{label}: </b> %{value}")
    fig.update_layout(autosize=False,
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0
        ),
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)