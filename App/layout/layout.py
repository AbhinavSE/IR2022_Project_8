from dash import html
from dash import dcc
from layout.navbar import navbar


content = html.Div(id="page-content")

layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content,
# background color: black
], style={"zoom": "75%", "background-image": "linear-gradient(to bottom right, #2b0980, #8069b8)"})
