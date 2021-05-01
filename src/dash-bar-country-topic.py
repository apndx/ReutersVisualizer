import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import base64
from io import BytesIO
import geopandas
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

f = open('data/drop_down_options.json',)
drop_down_options = json.load(f)

topic_fig = px.bar()
topic_fig.update_layout(clickmode='event+select')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#111111',
    'text': '#275f6b'
}

filename = "data/country_geo_topic_counts.gpkg"
reut_country_geo_topic = geopandas.read_file(filename)
reut_country_geo_topic.set_index('country', inplace=True)
reut_country_geo_topic['topiccounts'] = reut_country_geo_topic['topiccounts'].apply(
    eval)

app.layout = html.Div(children=[
    html.H1(children='Reuters topics', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
  html.Label('Dropdown'),
    dcc.Dropdown(
        id='my_dropdown',
        options= drop_down_options,
        value='AFGHANISTAN'
    ),
    dcc.Graph(id='country_topic')
])

@app.callback(
    Output(component_id='country_topic', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)
def update_country_topics(selected_country):
    country_dict = reut_country_geo_topic.loc[selected_country]['topiccounts']

    topic_keys = list(country_dict.keys())
    topic_values = list(country_dict.values())

    topic_fig = px.bar(x=topic_keys, y=topic_values, color=topic_values, height=800, labels={'x':'Topic', 'y':'Times used', 'color': 'Times used'})
    topic_fig.update_layout(transition_duration=500)
    return topic_fig

if __name__ == '__main__':
    app.run_server(debug=True)
