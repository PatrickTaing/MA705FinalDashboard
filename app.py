# -*- coding: utf-8 -*-
"""
@author: Pat
"""

import numpy as np
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=stylesheet)


df1 = pd.read_csv('winequality-red.csv', index_col=False, sep=';')
df2 =  pd.read_csv('winequality-white.csv', index_col=False, sep=';')

PAGE_SIZE = 5

attrNames = sorted(set(df1.columns))
attrNames.pop(attrNames.index('quality'))

df1_s = [df1.loc[:,[attr_type,'quality']] for attr_type in attrNames]
df2_s = [df1.loc[:,[attr_type,'quality']] for attr_type in attrNames]

df1_s = [df.groupby([df.columns[0]]).mean().reset_index() for df in df1_s]
df2_s = [df.groupby([df.columns[0]]).mean().reset_index() for df in df2_s]

df1_s = pd.concat(df1_s)
df2_s = pd.concat(df2_s)

style_dict = dict(width='50%',
                  height='25px',
                  textAlign='center',
                  fontSize=20)

# =============================================================================
# APP Layout
# =============================================================================
app.layout = html.Div([

    html.H1("Data Analytics on Two Variants of Wine", style={'text-align': 'center', 'font-family': 'verdana'}),
    html.Br(),
    html.H5("These two dataset today being analyzed refers back to the two red and white variants of Portugese wine.", style={'width': "100%",'text-align': 'left', 'font-family': 'verdana'}),
    html.H5("The dataset includes over 13 attribute information about the two wine variants.", style={'width': "100%",'text-align': 'left', 'font-family': 'verdana'}),
        html.A('Link to Data References',
           href='http://archive.ics.uci.edu/ml/datasets/Wine/wine.data',
           target='_blank',
           style={'float': 'right', 'font-family': 'verdana', 'font-size': '90%'}),
    html.H5("We can determine which wines are a lower quality or higher quality in comparison.", style={'width': "100%",'text-align': 'left', 'font-family': 'verdana'}),
    dcc.Dropdown(id="attr-type",
                 options = [dict([('label', attr.capitalize()), ('value', attr)]) for attr in attrNames],
                 multi=False,
                 value='alcohol',
                 style={'width': "30%", 'float': 'left'}
                 ),
    html.H2("Area Graphs", style={'width': "100%",'text-align': 'center', 'font-family': 'verdana', 'float': 'left'}),
    dcc.Graph(id='red-line', 
            style = {'width': "50%",'float':'left', 'border-color': 'gray', 'border-style': 'solid', 'border-right': 'none', 'border-left': 'none', 'border-size': 'thick'}),
    dcc.Graph(id='white-line', 
            style = {'width': "50%",'float':'right', 'border-color': 'gray', 'border-style': 'solid', 'border-right': 'none', 'border-left': 'none', 'border-size': 'thick'}),
    #html.Hr(style= {"width": "100%", "height": "2px", "text-align": "left", "margin-left": "0", "color": "white", "background-color": "white"}),
    html.H2("Scatterplot Graphs", style={'width': "100%",'text-align': 'center', 'font-family': 'verdana', 'float': 'left'}),
    dcc.Graph(id='red-scatter', 
            style = {'width': "50%", 'float':'left', 'border-color': 'gray', 'border-style': 'solid', 'border-right': 'none', 'border-left': 'none', 'border-size': 'thick'}),
    dcc.Graph(id='white-scatter', 
            style = {'width': "50%", 'float':'right', 'border-color': 'gray', 'border-style': 'solid', 'border-right': 'none', 'border-left': 'none', 'border-size': 'thick'}),
    html.Hr(style= {"width": "100%", "height": "2px", "text-align": "left", "margin-left": "0", "color": "white", "background-color": "white"})
])

# =============================================================================
# callbacks 
# =============================================================================
server = app.server

# Generation bar chart update
@app.callback(
    Output(component_id='red-line', component_property='figure'),
    Input(component_id='attr-type', component_property='value')
)
def update_genBar(attr_type):
    
    df = df1.copy()
    
    df = df.loc[:,[attr_type,'quality']]

    fig = px.area(
        df.groupby([attr_type]).mean().reset_index(),
        x = attr_type,
        y = "quality",
        title = attr_type.capitalize() + ' relation with Red Portugese Wine quality',
        )

    fig.update_layout(
        font_color="black",
        font_size = 12,
        title_font_color="Black",
        title_font_size = 18,
        legend_title_font_color="green",
        title = {'x': 0.05,'xanchor':'left'},
        paper_bgcolor = "#D3D3D3",
        xaxis_title=attr_type.capitalize(),
        yaxis_title="Quality",
        legend_title="Energy Source",
        bargap=0.2,
        yaxis_range=[0,10]
    )

    fig.update_xaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )

    fig.update_yaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )

    return fig

# Generation bar chart update
@app.callback(
    Output(component_id='white-line', component_property='figure'),
    Input(component_id='attr-type', component_property='value')
)
def update_genBar(attr_type):
    
    df = df2.copy()
    
    df = df.loc[:,[attr_type,'quality']]

    fig = px.area(
        df.groupby([attr_type]).mean().reset_index(),
        x = attr_type,
        y = "quality",
        title = attr_type.capitalize() + ' relation with White Portugese Wine quality',
        )

    fig.update_layout(
        font_color="black",
        font_size = 12,
        title_font_color="Black",
        title_font_size = 18,
        legend_title_font_color="green",
        title = {'x': 0.05,'xanchor':'left'},
        paper_bgcolor = "#D3D3D3",
        xaxis_title=attr_type.capitalize(),
        yaxis_title="Quality",
        legend_title="Energy Source",
        bargap=0.2,
        yaxis_range=[0,10]
    )

    fig.update_xaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )

    fig.update_yaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )

    return fig

# Generation bar chart update
@app.callback(
    Output(component_id='red-scatter', component_property='figure'),
    Input(component_id='attr-type', component_property='value')
)
def update_genBar(attr_type):
    
    df = df1_s.copy()
    
    fig = px.scatter(
        df,
        x = df.columns,
        y = "quality",
        title = 'Red Portugese Wine quality',
        )

    fig.update_layout(
        font_color="black",
        font_size = 12,
        title_font_color="Black",
        title_font_size = 18,
        legend_title_font_color="green",
        title = {'x': 0.05,'xanchor':'left'},
        paper_bgcolor = "#D3D3D3",
        xaxis_title='',
        yaxis_title="Quality",
        legend_title="Attributes",
        bargap=0.2,
    )

    fig.update_xaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )

    fig.update_yaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )

    return fig

# Generation bar chart update
@app.callback(
    Output(component_id='white-scatter', component_property='figure'),
    Input(component_id='attr-type', component_property='value')
)
def update_genBar(attr_type):
    
    df = df2_s.copy()
    
    fig = px.scatter(
        df,
        x = df.columns,
        y = "quality",
        title = 'White Portugese Wine quality',
        )

    fig.update_layout(
        font_color="black",
        font_size = 12,
        title_font_color="Black",
        title_font_size = 18,
        legend_title_font_color="green",
        title = {'x': 0.05,'xanchor':'left'},
        paper_bgcolor = "#D3D3D3",
        xaxis_title='',
        yaxis_title="Quality",
        legend_title="Attributes",
        bargap=0.2,
    )

    fig.update_xaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )

    fig.update_yaxes(
        tickfont=dict(family='Calibri', color='darkred', size=15)
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
