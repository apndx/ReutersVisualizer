import dash
import dash_core_components as dcc
import dash_html_components as html
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

# Opening JSON file
f = open('data/drop_down_options.json',)
  
# returns JSON object as 
# a dictionary
drop_down_options = json.load(f)
  
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#111111',
    'text': '#275f6b'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
filename = "data/country_geo_topic_counts.gpkg"
reut_country_geo_topic = geopandas.read_file(filename)
reut_country_geo_topic.set_index('country', inplace=True)
reut_country_geo_topic['topiccounts'] = reut_country_geo_topic['topiccounts'].apply(
    eval)

finland_dict = reut_country_geo_topic.loc['FINLAND']['topiccounts']

finland = plt.figure(figsize=(10, 10))
ax = finland.add_axes([0, 0, 1, 1])
ax.axis('off')

ax.margins(0)
reut_country_geo_topic.loc[['FINLAND']].plot('count', ax=ax)
plt.savefig('pics/finland.png', bbox_inches="tight", pad_inches=0)

finland_mask = np.array(Image.open("pics/finland.png"))
finland_cloud = WordCloud(background_color="white", mask=finland_mask,
                          width=1000, height=1000, contour_width=0.5)
finland_cloud.generate_from_frequencies(finland_dict)

wc_img = finland_cloud.to_image()
with BytesIO() as buffer:
    wc_img.save(buffer, 'png')
    img2 = base64.b64encode(buffer.getvalue()).decode()

app.layout = html.Div(children=[
    html.H1(children='Reuters topic wordclouds by countries', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
  html.Label('Dropdown'),
    dcc.Dropdown(
        options= drop_down_options,
        value='MTL'
    ),
    html.Img(src="data:image/png;base64," + img2),
])

if __name__ == '__main__':
    app.run_server(debug=True)
