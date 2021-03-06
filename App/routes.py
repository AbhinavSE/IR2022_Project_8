import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from app import app
from utils.constants import PATHS
from pages.music import music
from pages.about import about
from pages.add import add


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == PATHS['music']:
        return music.layout
    elif pathname == PATHS['add']:
        return add.layout
    elif pathname == PATHS['about']:
        return about.layout

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
