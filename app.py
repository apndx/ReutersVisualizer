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
from word_cloud_colors import Freq_colormap_color_func

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

f_country = open('data/country_options.json')
drop_down_options = json.load(f_country)
f_colours = open('data/color_options.json')
colorscales = json.load(f_colours)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

colors = {
    'background': '#111111',
    'text': '#275f6b'
}

left_style = {
    'color': colors['text'],
    'textAlign': 'left'
}

filename = "data/country_geo_topic_counts.gpkg"
reut_country_geo_topic = geopandas.read_file(filename)

reut_country_geo_topic.set_index('index', inplace=True)

reut_country_geo_topic['topiccounts'] = reut_country_geo_topic['topiccounts'].apply(
    eval)

app.layout = html.Div(children=[
    html.H1(id='title', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div([
        html.Div(children=[
            html.Table([
                html.Tr(
                    [
                        html.Td(html.Label('Choose the country',
                                           style={
                                               'color': colors['text'],
                                               'textAlign': 'left',
                                               'width': '60%'
                                           }), style={'border': 'none'}),
                        html.Td(html.Label('Choose the colour scale',
                                           style=left_style), style={'border': 'none'}),
                        html.Td(html.A('Info', href='https://github.com/apndx/ReutersVisualizer',
                                       style=left_style, target='_blank'), style={'border': 'none'}),
                    ]
                ),
                html.Tr(
                    [
                        html.Td(
                            dcc.Dropdown(
                                id='dropdown',
                                options=drop_down_options,
                                value='WORLD', style=left_style), style={'border': 'none', 'width': '60%'}),
                        html.Td(
                            dcc.Dropdown(
                                id='colorscale',
                                options=colorscales,
                                value='viridis', style=left_style), style={'border': 'none'})
                    ]),

            ])
        ]),

        html.Div([
            html.Div(dcc.Graph(id='country_topic'),
                     style={
                'backgroundColor': 'white',
                'margin-left': '10px',
                'width': '45%',
                'text-align': 'center',
                'display': 'inline-block',
                'vertical-align': 'top'
            }),
            html.Div(html.Img(id='cloud'),
                     style={
                'backgroundColor': 'white',
                'margin-left': '10px',
                'width': '45%',
                'text-align': 'center',
                'display': 'inline-block',
                'padding-top': '30px'
            }),
        ]),
    ])])


@app.callback(
    Output(component_id='cloud', component_property='src'),
    Input('dropdown', 'value'),
    Input('colorscale', 'value'))
def update_cloud(selected_country, scale):

    country_dict = reut_country_geo_topic.loc[selected_country]['topiccounts']

    country_fig = plt.figure(figsize=(7, 7))
    ax = country_fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.margins(0)

    own_colour_func = Freq_colormap_color_func(scale, country_dict)
    country_cloud = None
    has_geometry = reut_country_geo_topic.loc[selected_country]['geometry'] != None

    if has_geometry:
        reut_country_geo_topic.loc[[selected_country]].plot('count', ax=ax)
        plt.savefig(f'pics/{selected_country}.png',
                    bbox_inches="tight", pad_inches=0)
        country_mask = np.array(Image.open(f'pics/{selected_country}.png'))
        country_cloud = WordCloud(background_color="white", mask=country_mask,
                                  width=900, height=900, contour_width=0.5, color_func=own_colour_func)
    elif selected_country == 'WORLD':
        reut_country_geo_topic.plot('count', ax=ax)
        plt.savefig(f'pics/{selected_country}.png',
                    bbox_inches="tight", pad_inches=0)
        country_mask = np.array(Image.open(f'pics/{selected_country}.png'))
        country_cloud = WordCloud(background_color="white", mask=country_mask,
                                  width=900, height=900, contour_width=0.5, color_func=own_colour_func)
    else:
        country_cloud = WordCloud(
            background_color="white", width=700, height=700, color_func=own_colour_func)

    country_cloud.generate_from_frequencies(country_dict)
    wc_img = country_cloud.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        cloud_fig = base64.b64encode(buffer.getvalue()).decode()

    src = "data:image/png;base64," + cloud_fig
    plt.clf()
    plt.close(country_fig)
    return src


@app.callback(
    Output(component_id='country_topic', component_property='figure'),
    Input('dropdown', 'value'),
    Input('colorscale', 'value'))
def update_country_topics(selected_country, scale):

    scale = scale.lower()
    country_dict = reut_country_geo_topic.loc[selected_country]['topiccounts']

    topic_keys = list(country_dict.keys())
    topic_values = list(country_dict.values())

    topic_fig = px.bar(x=topic_keys, y=topic_values, color=topic_values, height=800, labels={
        'x': 'Topic', 'y': 'Times used', 'color': 'Times used'}, color_continuous_scale=scale)
    topic_fig.update_layout(transition_duration=500)
    return topic_fig


@app.callback(
    Output(component_id='title', component_property='children'),
    Input('dropdown', 'value')
)
def update_output_div(selected_country):
    if selected_country == 'WORLD':
        return 'Reuters topics for the World'
    else:
        return 'Reuters topics for {}'.format(selected_country.title())

if __name__ == '__main__':
    app.run_server(debug=True)
