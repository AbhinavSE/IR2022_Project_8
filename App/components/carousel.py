import dash_bootstrap_components as dbc
from dash import html


def get_carousel():
    """
    items: contains a list of dicts with the following keys:
        - src: the image source
        - header: the header text
        - caption: the caption text
    """

    return html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Carousel(
                    id='music-carousel-slides',
                    items=[],
                    variant="dark",
                    indicators=True,
                    controls=True,
                    interval=5000,
                    style={'width': '60%', 'margin': 'auto'}
                ), width=8
            )
        ], justify='center'),
        html.Br(),
        dbc.Row([
            # Title and Header
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        html.Div(id='music-carousel-title', style={'color': 'white', 'font-weight': 'bold'}),
                    )
                ], style={'text-align': 'right'}),
                dbc.Row([
                    dbc.Col(
                        html.Div(id='music-carousel-artist', style={'color': 'white', 'font-style': 'italic'}),
                    )
                ], style={'text-align': 'right'}),
            ]),
            # Play button
            dbc.Col(
                dbc.Button(
                    id=f"music-carousel-play-btn",
                    children="▶ Play",
                    color="primary",
                    # Rounded Border with green background and white text
                    style={'background-color': '#005555', 'color': 'white', 'borderRadius': '10px',
                           'overflow': 'hidden', 'background-color': "green", "font-size": "1.2rem", "padding": "0.5rem",
                           'position': 'relative', 'top': '50%', 'transform': 'translateY(-50%)'}
                ),
            ),

        ]),
        html.Br(),
    ], style={'background-color': '#161617'})
