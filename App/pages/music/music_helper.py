from utils.data import isSongLiked
from app import app
from dash import html
from dash.dependencies import Input, Output, State
from components.carousel import get_carousel
import dash_bootstrap_components as dbc
from utils.data import load_music
from components.cards import get_music_card


def get_recommended_songs_carousel():
    def recommended_songs():
        music = load_music()
        items = []
        for song in music:
            items.append({'src': song['image_folder'], 'title': song['Title'], 'artist': song['Artist']})
        return items

    items = recommended_songs()
    return get_carousel(items)


def getMusicCards(music):
    cards = []
    card_i = 0
    if len(music) < 15:
        music.extend([{'Id': 'None', 'Title': 'None', 'Artist': 'None', 'image_folder': 'None'} for i in range(15 - len(music))])
    liked = isSongLiked([m['Id'] for m in music])

    for i in range(0, 15, 5):
        length = min(len(music), i + 5) - i
        cards.append(
            dbc.Row(
                [dbc.Col(get_music_card(i=c, song_id=music[j]['Id'], title=music[j]['Title'], artist=music[j]['Artist'],
                                        img_loc=music[j]['image_folder'], like=liked[c])
                         ) for c, j in zip(range(card_i, card_i + length), range(i, i + length))
                 ]
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
                        dbc.Input(id='music-search-text', type='text', className='form-control', placeholder='Search...',
                                  style={'background-color': '#1d1d1d', 'color': 'white', 'border': '1px solid black',
                                         'borderRadius': '15px', 'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000',
                                         'width': '70%'}
                                  ),
                        dbc.Select(id='music-search-type', options=[
                            {'label': 'Title', 'value': 'Title'},
                            {'label': 'Artist', 'value': 'Artist'},
                            {'label': 'Lyrics', 'value': 'Lyrics'},
                        ], value='Title',
                            style={'background-color': '#1d1d1d', 'color': 'white', 'border': '1px solid black', 'borderRadius': '15px',
                                   'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000'}),
                    ], size='md'
                    ),
                    html.Div(id='music-search-out')
                ]
            )
        ]
    )
