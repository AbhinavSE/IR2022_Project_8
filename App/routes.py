import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from app import app
from utils.constants import PATHS
import index
# from pages.logs import logs


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == PATHS['index']:
        return index.layout

    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
