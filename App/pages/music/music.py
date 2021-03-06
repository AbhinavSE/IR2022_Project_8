from dash import html, dcc
from components.carousel import get_carousel
from utils.constants import *
import dash_bootstrap_components as dbc
from pages.music.music_helper import search_bar
from pages.music.music_callbacks import *

layout = html.Div([
    get_carousel(),
    html.Br(),
    html.Br(),
    html.Div(
        id='music-search',
        children=[search_bar()],
        # crop height
        style={'width': '90%', 'margin': 'auto', 'height': '50px'}
    ),
    html.Br(),
    html.Br(),
    html.Div(
        id='music-cards',
        children=[],
        style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '80%'}
    ),
    # Pagination
    html.Div([
        # center
        dbc.Pagination(id='music-pagination', active_page=1, max_value=24, fully_expanded=False),
    ], style={'width': '20%', 'margin': 'auto', 'height': '50px'},
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    # Music player in the bottom as fixed footer
    html.Footer(
        children=[
            html.Br(),
            dbc.Row([
                # small width
                dbc.Col([
                    html.Img(id='music-player-cover-img', src='assets/album_covers/faded.jpg', style={'width': '100px'}),
                ], width=2, style={'text-align': 'right'}),
                dbc.Col([
                    dbc.Row(
                        dbc.Col(
                            [
                                # Bold Title, align to left
                                html.H4(id='music-player-title', style={'color': 'white', 'font-weight': 'bold'}),
                            ]
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            [
                                # italic
                                html.P(id='music-player-artist', style={'color': 'white', 'font-style': 'italic'}),
                            ]
                        )
                    ),
                    dbc.Row([
                        dbc.Col(
                            [
                                # Audio player centered and slightly thicker
                                html.Audio(
                                    id='music-player-audio',
                                    src='assets/music/music.mp3', controls=True,
                                    # autoPlay=True,
                                    style={'width': '80%', 'border': '1px solid black', 'borderRadius': '15px',
                                           'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000'
                                           }
                                ),
                            ]
                        )
                    ])
                ]),
            ]),

        ],
        # Center the footer content
        style={'background-color': 'black', 'color': 'white', 'position': 'fixed', 'bottom': '0', 'width': '100%', 'height': '150px',
               'border': '1px solid black', 'borderRadius': '15px', 'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000', 'zIndex': '1'}
    ),
])
