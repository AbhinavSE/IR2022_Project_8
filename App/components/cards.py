import dash_bootstrap_components as dbc
from dash import html

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