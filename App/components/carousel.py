import dash_bootstrap_components as dbc


def get_carousel(items):
    """
    items: contains a list of dicts with the following keys:
        - src: the image source
        - header: the header text
        - caption: the caption text
    """

    for i in range(len(items)):
        items[i]['key'] = i + 1
    # adjust size with black bars on the sides with 50% of the width
    
    return dbc.Row([
        dbc.Col(
            dbc.Carousel(
                items=items,
                variant="dark",
                indicators=True,
                controls=True,
                interval=2000,
                style={'width': '50%', 'margin': 'auto'}
            ), width=8
        )
    ], justify='center', style={'background-color': '#1d1d1d'})
