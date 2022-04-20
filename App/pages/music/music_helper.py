from dash import html
from components.carousel import get_carousel
import dash_bootstrap_components as dbc
from utils.data import load_music
from components.cards import get_card


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
    

def music_cards():
    music = load_music()
    cards = []
    for i in range(0, len(music), 5):
        cards.append(
            dbc.Row(
                [dbc.Col([get_card(music[i]['song'], music[i]['artist'], music[i]['img'], '#')]) for i in range(i, min(len(music), i+5))]
            )
        )
        cards.append(html.Br())
    return cards

    
