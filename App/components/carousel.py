import dash_bootstrap_components as dbc


def get_carousel():
    """
    items: contains a list of dicts with the following keys:
        - src: the image source
        - header: the header text
        - caption: the caption text
    """

    return dbc.Row([
        dbc.Col(
            dbc.Carousel(
                id='music-carousel',
                items=[],
                variant="dark",
                indicators=True,
                controls=True,
                interval=2000,
                style={'width': '60%', 'margin': 'auto'}
            ), width=8
        )
    ], justify='center', style={'background-color': '#161617'})
