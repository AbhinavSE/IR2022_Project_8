from dash import html
from components.jumbotron import get_jumbotron
from utils.constants import *
from components.cards import get_card
import dash_bootstrap_components as dbc
from pages.music.music_helper import get_recommended_songs_carousel

layout = html.Div([
    get_recommended_songs_carousel(),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(
            dbc.Row([
                get_card("Twitter", "Get Latest cloud news from twitter", 'https://i.imgur.com/3wi2lbT.png', '#'),
                get_card("Google", "Get Latest cloud news from google", 'https://i.imgur.com/IL9caLK.jpeg', '#'),
            ])
        ),
    ],
        style={
        "align-items": "center",
        "justify-content": "center",
        "display": "flex",
        "flex-direction": "row",
        "flex-wrap": "wrap",
        "margin-top": "20px",
        "margin-bottom": "20px",
    },
    ),
])
