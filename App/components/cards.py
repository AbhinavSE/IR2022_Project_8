import dash_bootstrap_components as dbc
from dash import html

def get_card(title, body, img_loc, href):
    """
    title, body, img_loc, href of card
    """
    return dbc.Card([
        dbc.CardImg(src=img_loc, top=True),
        html.Audio(src='assets/music/music.mp3', controls=True, style={'width': '100%'}),
        dbc.CardBody([
            html.H4(title, className="card-title"),
            html.P(
                body,
                className="card-text",
            ),
            dbc.Input(type="button", value="👍 Like", ),
        ]),
    ],
                    # gray
    style={"width": "18rem", "background-color": "#DCDCDC"},
)
