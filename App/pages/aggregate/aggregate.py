from dash import html
from pages.aggregate.sidebar.sidebar import sidebar
from components.jumbotron import get_jumbotron
from pages.aggregate.sections.tags import tags
from pages.aggregate.sections.news import news
from pages.aggregate.sections.trends import trends
from utils.constants import *


news_layout = html.Div(children=[
    sidebar,
    html.Div([
        get_jumbotron('Aggregated Cloud News', 'Top Cloud News', 'Filtered, Labeled, and Scored'),
        html.Br(),
        html.Div(id='aggregate-content', children=news.layout),
    ], style=CONTENT_STYLE)
])

tags_layout = html.Div(children=[
    sidebar,
    html.Div([
        get_jumbotron('Aggregated Cloud Tags', 'Top Cloud News', 'Filtered, Labeled, and Scored'),
        html.Br(),
        html.Div(id='aggregate-content', children=tags.layout),
    ], style=CONTENT_STYLE)
])

trends_layout = html.Div(children=[
    sidebar,
    html.Div([
        get_jumbotron('Aggregated Cloud Trends', 'Top Cloud News', 'Filtered, Labeled, and Scored'),
        html.Br(),
        html.Div(id='aggregate-content', children=trends.layout),
    ], style=CONTENT_STYLE)
])
