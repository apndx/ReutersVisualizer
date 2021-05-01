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
    html.H1(children='Reuters topics by countries', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
  html.Label('Dropdown'),
    dcc.Dropdown(
        id='dropdown',
        options= drop_down_options,
        value='AFGHANISTAN'
    ),
    html.Img(id='cloud'),
    dcc.Graph(id='country_topic')
])

@app.callback(
    Output(component_id='cloud', component_property='src'),
    Input('dropdown', 'value'))
def update_cloud(selected_country):

    country_dict = reut_country_geo_topic.loc[selected_country]['topiccounts']

    country_cloud = None
    country_fig = plt.figure(figsize=(8, 8))
    ax = country_fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.margins(0)

    has_geometry = reut_country_geo_topic.loc[selected_country]['geometry'] != None

    if has_geometry:
        reut_country_geo_topic.loc[[selected_country]].plot('count', ax=ax)
        plt.savefig(f'pics/{selected_country}.png', bbox_inches="tight", pad_inches=0)
        country_mask = np.array(Image.open(f'pics/{selected_country}.png'))
        country_cloud = WordCloud(background_color="white", mask=country_mask,
                width=900, height=900, contour_width=0.5)

    else:
        country_cloud = WordCloud(background_color="white", width=900, height=900)

    country_cloud.generate_from_frequencies(country_dict)
    wc_img = country_cloud.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        cloud_fig = base64.b64encode(buffer.getvalue()).decode()

    src="data:image/png;base64," + cloud_fig

    return src

@app.callback(
    Output(component_id='country_topic', component_property='figure'),
    Input('dropdown', 'value'))
def update_country_topics(selected_country):
    country_dict = reut_country_geo_topic.loc[selected_country]['topiccounts']

    topic_keys = list(country_dict.keys())
    topic_values = list(country_dict.values())

    topic_fig = px.bar(x=topic_keys, y=topic_values, color=topic_values, height=800, labels={'x':'Topic', 'y':'Times used', 'color': 'Times used'})
    topic_fig.update_layout(transition_duration=500)
    return topic_fig


if __name__ == '__main__':
    app.run_server(debug=True)
