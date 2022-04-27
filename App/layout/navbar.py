import dash_bootstrap_components as dbc
from utils.constants import PATHS
from dash import html

# Add logo
navbar = dbc.NavbarSimple(
    className='sticky-top',
    children=[
        dbc.NavItem(dbc.NavLink("Music", href=PATHS['music'])),
        dbc.NavItem(dbc.NavLink("Add", href=PATHS['add'])),
    ],
    brand="RECOM",
    color="black",
    dark=True,
    links_left=True,
)
