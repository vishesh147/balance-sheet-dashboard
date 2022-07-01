from __future__ import annotations
from turtle import width
from dash import Dash, dash_table, dcc, html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from BalanceSheetScraper import BalanceSheet as bs
from BalanceSheetScraper import *


app = Dash(__name__)


# Bar Plot

fig = go.Figure(
    data=[
        go.Bar(name='Total Debt', x=bs['Year'].to_list(), y=bs['Total Long Term Debt'].to_list()),
        go.Bar(name='Total Equity', x=bs['Year'].to_list(), y=bs['Total Equity'].to_list())],
    )

fig.update_layout(barmode='group', title='Debt-to-Equity')
fig.update_xaxes(fixedrange=True)
fig.update_yaxes(fixedrange=True)

# Donut

DERatio = [i/j for i, j in zip(bs['Total Long Term Debt'].to_list(), bs['Total Equity'].to_list())]

fig2 = px.pie(
    data_frame=bs,
    names=['Total Equity', 'Total Debt'],
    labels=['Total Equity', 'Total Debt'],
    values=[bs['Total Equity'].to_list()[-1], bs['Total Long Term Debt'].to_list()[-1]],
    hole=.6,
    title='Debt-To-Equity Ratio',
)


fig2.add_annotation(x=0.5, y=0.5,
    text="<b>%.2f</b>" % DERatio[-1],
    font_size=30,
    showarrow=False,
    )
fig2.update_traces(textinfo='none', hovertemplate= "<b>%{label}: </b> %{value}")


# Line chart
fig3 = px.line(
    data_frame={
        "Year":bs['Year'].to_list(),
        "D/E Ratio":DERatio,
        "TotalDebt":bs['Total Long Term Debt'].to_list(),
        "TotalEquity":bs['Total Equity'].to_list(),
    },
    text=["<b>%.2f<b>" %s for s in DERatio],
    x="Year", 
    y="D/E Ratio",
    custom_data = ['TotalDebt', 'TotalEquity'],
    range_y=[min(DERatio) - 0.5, max(DERatio) + 0.5], 
    range_x=[-.4, 3.5],
    markers=True,
    )

fig3.update_traces(
    textposition="top center", 
    textfont_size=14,
    hovertemplate= "<b>%{x}</b><br><br><b>Quick Assets:</b> %{customdata[0]}<br><b>Current Liabilities:</b> %{customdata[1]}"
    )
fig3.update_xaxes(showgrid=False, tickfont=dict(size=14), fixedrange=True)
fig3.update_yaxes(showticklabels=False, showgrid=False, fixedrange=True, zeroline=False)


app.layout = html.Div([
    dcc.Graph(figure=fig, style={'height':'70vh', 'width':'100vh'}, config={'displaylogo': False}),
    dcc.Graph(figure=fig2, style={'height':'70vh', 'width':'70vh'}, config={'displaylogo': False}),
    dcc.Graph(figure=fig3, style={'width': '80vh', 'height': '50vh'}, config={'displaylogo': False})
])

if __name__ == '__main__':
    app.run_server(debug=True)
