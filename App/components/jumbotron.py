from dash import html
import dash_bootstrap_components as dbc


def get_jumbotron(title, caption1=None, caption2=None):
    return html.Div(
        dbc.Container(
            [
                html.H1(title, className="display-3"),
                html.P(
                    caption1,
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    caption2
                ),
                html.P(
                    dbc.Button("Learn more", color="primary"), className="lead"
                ),
            ],
            fluid=True,
            className="py-3",
        ),
        className="p-3 bg-light rounded-3",
    )
