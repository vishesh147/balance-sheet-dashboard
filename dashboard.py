from __future__ import annotations
from turtle import width
from dash import Dash, dash_table, dcc, html, Input, Output
from numpy import pad, sort
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from BalanceSheetScraper import BalanceSheet as bs
from BalanceSheetScraper import *
import pandas as pd

app = Dash(__name__)

figbar = go.Figure(data=[
    go.Bar(name='Total Equity', x=bs["Year"].to_list(), y=bs["Total Equity"].to_list()),
    go.Bar(name='Total Liabilities', x=bs["Year"].to_list(), y=bs["Total Liabilities"].to_list()),
    go.Bar(name='Total Assets', x=bs["Year"].to_list(), y=bs["Total Assets"].to_list()),
])
figbar.update_layout(autosize=True,
    margin=dict(
    l=10,
    r=10,
    b=10,
    t=10,
    pad=0
    ),
)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label(companyName+": An Overview", className='company'),
            dcc.Graph(figure=figbar, id='barchart', style={'height':'90%'}, config={'displaylogo': False})
        ], style={'width':'50%', 'padding-right':'50px'}),

        html.Div([
            html.Div([ 
                html.Label("Liquidity Ratios:", className='dropdown-label'), 
                dcc.Dropdown(
                    options=[
                        {'label': 'Current Ratio', 'value': "Current Ratio,Total Current Assets,Total Current Liabilities"},
                        {'label': 'Quick Ratio', 'value': "Quick Ratio,Quick Assets,Total Current Liabilities"},
                    ],
                    value="Current Ratio,Total Current Assets,Total Current Liabilities",
                    id='liquidity-ratio',
                    style={'width':'60%'},
                )
            ], className='dropdown-container'),
            html.Div([
                dcc.Graph(id='liquidity-ratio-pie', config={'displaylogo': False}, style={'width':'50%'}),
                dcc.Graph(id='liquidity-ratio-line', config={'displaylogo': False}, style={'width':'50%', 'height':'40vh'}),
            ], style={'display':'flex'}),
        ], style={'width':'50%'}),
    ], className='container'),
    
    html.Div([
        html.Div([
            html.Div([
                html.Label("Component: ", className='dropdown-label'),
                dcc.Dropdown(
                    [
                        'Cash & Equivalents',
                        'Total Inventory',
                        'Total Receivables, Net',
                        'Total Current Assets',
                        'Long Term Investments',
                        'Total Assets',
                        'Accounts Payable',
                        'Total Current Liabilities',
                        'Total Long Term Debt',
                        'Deferred Income Tax',
                        'Total Liabilities',
                        'Total Equity',
                    ],
                    
                    value='Cash & Equivalents',
                    id='line-data',
                    style={'width':'60%'}
                )
            ],  className='dropdown-container'),
            dcc.Graph(id='linechart', style={'height':'40vh'}, config={'displaylogo': False})
        ], style={'width':'50%', 'padding-right':'50px'}),

        html.Div([
            html.Div([ 
                html.Label("Leverage Ratios:", className='dropdown-label'), 
                dcc.Dropdown(
                    options=[
                        {'label': 'Debt-to-Equity Ratio', 'value': "DE Ratio,Total Long Term Debt,Total Equity"},
                        {'label': 'Debt-to-Assets Ratio', 'value': "DA Ratio,Total Long Term Debt,Total Assets"},
                    # {'label': 'Debt-to-Capital Ratio', 'value': "DC Ratio,Total Long Term Debt,Total Equity"},
                    ],
                    value="DE Ratio,Total Long Term Debt,Total Equity",
                    id='leverage-ratio',
                    style={'width':'60%'},
                )
            ], className='dropdown-container'),
            html.Div([
                dcc.Graph(id='leverage-ratio-pie', config={'displaylogo': False}, style={'width':'50%'}),
                dcc.Graph(id='leverage-ratio-line', config={'displaylogo': False}, style={'width':'50%', 'height':'40vh'}),
            ], style={'display':'flex'}),
        ], style={'width':'50%'}),
    ], className='container')
])

@app.callback(
    Output('linechart', 'figure'),
    Input('line-data', 'value'))
def update_graph(data):
    fig = px.line(data_frame=bs, x='Year', y=data, markers=True)
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
    Output('liquidity-ratio-line', 'figure'),
    Input('liquidity-ratio', 'value'))
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
    Output('liquidity-ratio-pie', 'figure'),
    Input('liquidity-ratio', 'value'))
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
        font_size=25,
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



@app.callback(
    Output('leverage-ratio-line', 'figure'),
    Input('leverage-ratio', 'value'))
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
    Output('leverage-ratio-pie', 'figure'),
    Input('leverage-ratio', 'value'))
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
        font_size=25,
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