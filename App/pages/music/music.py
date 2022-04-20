from dash import html
from components.jumbotron import get_jumbotron
from utils.constants import *
from components.cards import get_card
import dash_bootstrap_components as dbc
from pages.music.music_helper import get_recommended_songs_carousel, music_cards

layout = html.Div([
    get_recommended_songs_carousel(),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(
            music_cards()
        ),
    ], style={
        "align-items": "center",
        "justify-content": "center",
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "wrap",
        "margin-top": "20px",
        "margin-bottom": "20px",
    }),
])
