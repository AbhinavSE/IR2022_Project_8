import dash_bootstrap_components as dbc
from utils.constants import PATHS
from dash import html

# Add logo
navbar = dbc.NavbarSimple(
    className='sticky-top',
    children=[
        dbc.NavItem(dbc.NavLink("Music", href=PATHS['music'])),
        dbc.NavItem(dbc.NavLink("Add", href=PATHS['add'])),
        dbc.NavItem(dbc.NavLink("About", href=PATHS['about'])),
        # Logged in
        dbc.NavItem(dbc.NavLink("Logout", href='#')),
    ],
    brand="RECOM",
    color="black",
    dark=True,
    links_left=True,
)
