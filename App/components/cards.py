import dash_bootstrap_components as dbc
from dash import html


def get_card(title, body, img_loc, href):
    """
    title, body, img_loc, href of card
    """
    return dbc.Card([
        dbc.CardImg(src=img_loc, top=True),
        # Show only on hover
        html.Audio(src='assets/music/music.mp3', controls=True, style={'width': '100%'}),
        dbc.CardBody([
            html.H4(title, className="card-title"),
            html.P(
                body,
                className="card-text",
            ),
            # reduce vertical and horizontal padding
            # Liked:❤️ Default: 🤍
            dbc.Button("🤍", color="primary", href=href, style={'background-color': '#005555', 'color': 'white', 'borderRadius': '15px',
                                                               'overflow': 'hidden', 'background-color': "#1d1d1d", "font-size": "1.5rem", "padding": "0.5rem"}),
        ],
            # gray
        )
    ],
        # Magnify on hover
        style={"width": "100%", "background-color": "#1d1d1d", "color": "white", 'border': '1px solid black',
               'borderRadius': '15px',
               'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000'},
    )
