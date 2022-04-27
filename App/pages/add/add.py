from .add_callbacks import *
from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    html.Br(),
    html.Br(),
    html.H1('Add Song To Database', style={'text-align': 'center', 'color': '#ffffff', 'font-weight': 'bold'}),
    html.Br(),
    html.Div([
        dbc.InputGroup([
            dbc.InputGroupText("Title", style={'background-color': '#1d1d1d', 'color': 'white', 'borderRadius': '15px'}),
            dbc.Input(id='add-song-title', type='text', placeholder='Enter a song name'),
        ]),
        html.Br(),
        dbc.InputGroup([
            dbc.InputGroupText("Artist", style={'background-color': '#1d1d1d', 'color': 'white', 'borderRadius': '15px'}),
            dbc.Input(id='add-song-artist', type='text', placeholder='Enter an artist name'),
        ]),
        html.Br(),
        dbc.InputGroup([
            dbc.InputGroupText("Song", style={'background-color': '#1d1d1d', 'color': 'white', 'borderRadius': '15px'}),
            dcc.Upload(
                id='add-song-mp3',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
            )
        ], style={'justifyContent': 'center'}),
        html.Br(),
        dcc.Loading([
            dbc.Button('Add Song', id='add-song-button', color='primary', style={'background-color': '#1d1d1d', 'color': 'white',
                                                                                 'borderRadius': '15px', 'width': '100%'}),
            html.Br(),
            dbc.Alert(id='add-song-alert', color='danger', style={'display': 'none'}),
        ])
    ], style={'width': '50%', 'margin': 'auto'}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
])
