from dash import html
from components.jumbotron import get_jumbotron
from utils.constants import *
from components.cards import get_card
import dash_bootstrap_components as dbc
from pages.music.music_helper import get_recommended_songs_carousel, music_cards, search_bar

layout = html.Div([
    get_recommended_songs_carousel(),
    html.Br(),
    html.Br(),
    html.Div(
        children=[search_bar()],
        style={'width': '80%', 'margin': 'auto'}
    ),
    html.Br(),
    html.Div(
        children=music_cards(),
        style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '80%'}
    )
])
