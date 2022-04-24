import dash_bootstrap_components as dbc
from dash import html
from mpld3 import display
from utils.caching import cache, TIMEOUT


def get_music_card(i, song_id, title, artist, img_loc, like):
    """
    i, title, artist, img_loc of card
    """
    return dbc.Card(id=f'music-card-{i}', children=[
        dbc.CardImg(src=img_loc, top=True),
        # Show only on hover
        dbc.CardBody([
            html.H4(title[:30] + ('...' if len(title) > 30 else ''), className="card-title"),
            html.P(
                artist,
                className="card-text",
            ),
            dbc.Row([
                dbc.Col(
                    # reduce vertical and horizontal padding
                    # Liked:❤️ Default: 🤍
                    dbc.Button(
                        id=f"music-card-{i}-like-btn",
                        children="❤️" if like else "🤍",
                        color="primary",
                        style={'background-color': '#005555', 'color': 'white', 'borderRadius': '15px',
                               'overflow': 'hidden', 'background-color': "#1d1d1d", "font-size": "1.5rem", "padding": "0.5rem"}
                    ),
                ),
                # Play button
                dbc.Col(
                    dbc.Button(
                        id=f"music-card-{i}-play-btn",
                        children="▶️",
                        color="primary",
                        style={'background-color': '#005555', 'color': 'white', 'borderRadius': '15px',
                               'overflow': 'hidden', 'background-color': "#1d1d1d", "font-size": "1.5rem", "padding": "0.5rem"}
                    ),
                ),
            ]),
            html.Div(id=f'music-card-{i}-song-id', children=song_id, style={'display': 'none'}),
        ]),
    ],
        # Magnify on hover
        style={"width": "100%", "height": "100%",
               "background-color": "#1d1d1d", "color": "white", 'border': '1px solid black',
               'borderRadius': '15px',
               'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000'},
    )
