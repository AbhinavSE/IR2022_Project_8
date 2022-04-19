from app import app
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import os
from utils.constants import PATHS


def get_card(title, body, img_loc, href):
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardImg(src=img_loc, top=True, style={'height': '20rem', 'width': '100%'}),
                dbc.CardBody(
                    [
                        html.H4(title, className="card-title"),
                        html.P(
                            body,
                            className="card-text",
                        ),
                        dbc.Button("Explore", color="primary", href=href),
                    ]
                ),
            ],
            style={
                "width": "18rem",
                "height": "30rem",
            }
        )
    )


layout = dbc.Card(
    [
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
)
