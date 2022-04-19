import dash_bootstrap_components as dbc
from utils.constants import PATHS

navbar = dbc.NavbarSimple(
    className='sticky-top',
    children=[
        dbc.NavItem(dbc.NavLink("Music", href=PATHS['index'])),
        dbc.NavItem(dbc.NavLink("Recommendations", href=PATHS['index'])),
        # dbc.DropdownMenu(
        #     # children=[
        #     #     dbc.DropdownMenuItem("News", href='#'),
        #     #     dbc.DropdownMenuItem("Tags", href='#'),
        #     #     dbc.DropdownMenuItem("Trends", href='#'),
        #     # ],
        #     nav=True,
        #     in_navbar=True,
        #     label="",
        # ),
    ],
    brand="RECOM",
    brand_href="#",
    color="primary",
    dark=True,
    links_left=True,
)
