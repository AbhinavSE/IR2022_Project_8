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

    return dbc.Carousel(
        items=items,
        variant="dark",
        indicators=True,
        controls=True,
        style={
            # adjust size
            "width": "50%",
            "height": "50%",
            "margin-left": "auto",
            "margin-right": "auto",
            "margin-top": "20px",
            "margin-bottom": "20px",
            "align-items": "center",

        }
    )
