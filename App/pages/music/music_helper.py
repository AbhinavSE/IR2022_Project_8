from app import app
from dash import html
from dash.dependencies import Input, Output, State
from components.carousel import get_carousel
import dash_bootstrap_components as dbc
from utils.data import load_music
from components.cards import get_music_card


def get_recommended_songs_carousel():
    items = [
        {
            'src': 'assets/album_covers/stereo_hearts.jpeg',
            'header': 'Stereo Hearts',
            'caption': '~Gym Class Heroes',
        },
        {
            'src': 'assets/album_covers/faded.jpg',
            'header': 'Faded',
            'caption': '~Alan Walker',
        }
    ]
    return get_carousel(items)


def music_cards(page, likes_status):
    page = 0 if not page else page - 1
    music = load_music()
    cards = []
    card_i = 0
    for i in range(page * 15, (page + 1) * 15, 5):
        length = min(len(music), i + 5) - i
        cards.append(
            dbc.Row(
                [dbc.Col([get_music_card(i=c, song_id=j, title=music[j]['Title'], artist=music[j]['Artist'], img_loc=music[j]['image_folder'], like=(str(j) in likes_status))])
                 for c, j in zip(range(card_i, card_i + length), range(i, min(len(music), i + 5)))]
            )
        )
        cards.append(html.Br())
        card_i += length

    return cards


def search_bar():
    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.InputGroup([
                        dbc.InputGroupText("Search Songs", style={'background-color': '#1d1d1d', 'color': 'white', 'borderRadius': '15px'}),
                        # text-input
                        dbc.Input(id='search-button', type='text', className='form-control', placeholder='Search...',
                                  style={'background-color': '#1d1d1d', 'color': 'white', 'border': '1px solid black', 'borderRadius': '15px', 'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000'}),
                    ], size='md'
                    )
                ]
            )
        ]
    )
