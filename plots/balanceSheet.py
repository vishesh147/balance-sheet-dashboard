from __future__ import annotations
from dash import Dash, dash_table, dcc, html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from BalanceSheetScraper import *

df = balanceSheet["currAssets"]

app = Dash(__name__)

app.layout = dash_table.DataTable(
    id='curr-assets-datatable',
    columns=[
        {'name': i, 'id': i} for i in df.columns
        # omit the id column
        if i != 'id'
    ],
    data=df.to_dict('records'),
    fixed_rows={'headers': True},
    style_cell={
        'padding': 10,
        'fontSize': 14, 
        'font-family':'Sans-Serif',
    },
    style_header={
        'backgroundColor': 'rgb(10, 10, 10)',
        'color': 'white',
        'fontWeight': 'bold'
    },
    style_data={
        'backgroundColor': 'rgb(10, 10, 30)',
        'color': 'white',
        'border': '1px solid gray'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 9},
                'fontWeight': 'bold'
        },
    ],
    style_cell_conditional=[
        {'if': {'column_id': df.columns[0]},
            'width': '40%'
         },
        {'if': {'column_id': df.columns[0]},
            'textAlign': 'left'
        }
    ],
    style_table={
        'borderRadius': '15px',
        'overflow': 'hidden',
        'width': '50%',
        'height': 'auto'
    },
    style_as_list_view=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)
