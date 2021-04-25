import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud
import base64
from io import BytesIO

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
reut_country_geo_topic = pd.read_csv('csv/country_geo_topic_counts.csv', delimiter=';')
reut_country_geo_topic.set_index('country', inplace=True)
reut_country_geo_topic['topiccounts'] = reut_country_geo_topic['topiccounts'].apply(eval)
finland_dict =  reut_country_geo_topic.loc['FINLAND']['topiccounts']

wc = WordCloud(background_color="white").generate_from_frequencies(finland_dict)
wc_img = wc.to_image()
with BytesIO() as buffer:
    wc_img.save(buffer, 'png')
    img2 = base64.b64encode(buffer.getvalue()).decode()

app.layout = html.Div(children=[
                    html.Img(src="data:image/png;base64," + img2)
])

if __name__ == '__main__':
    app.run_server(debug=True)
