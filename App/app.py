import dash
import dash_bootstrap_components as dbc
from flask import Flask
import os

server = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'assets'))

app = dash.Dash(__name__,
                server=server,
                external_stylesheets=[dbc.themes.SLATE])
app.config.suppress_callback_exceptions = True
