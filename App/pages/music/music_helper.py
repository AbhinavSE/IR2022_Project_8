from utils.data import isSongLiked
from app import app
from dash import html
from dash.dependencies import Input, Output, State
from components.carousel import get_carousel
import dash_bootstrap_components as dbc
from utils.data import load_music, getLikes, getRecommender
from components.cards import get_music_card


def getRecommenedSongs():
    music = load_music()
    songs_liked = list(getLikes().keys())
    songs_liked = [int(s) for s in songs_liked]
    items = []
    if len(songs_liked) > 0:
        rec = getRecommender()
        user_vector = rec.generate_user_vector(songs_liked)
        recommendations = rec.get_recommendations(user_vector)
        for s_id in recommendations:
            items.append({'src': music[s_id]['image_folder'], 'title': music[s_id]['Title'], 'artist': music[s_id]['Artist'], 'id': s_id})
    return items


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
                                  persistence=True, persistence_type='memory',
                                  style={'background-color': '#1d1d1d', 'color': 'white', 'border': '1px solid black',
                                         'borderRadius': '15px', 'overflow': 'hidden', 'boxShadow': '0px 0px 10px #000000',
                                         'width': '70%'}
                                  ),
                        dbc.Select(id='music-search-type', options=[
                            {'label': 'Title', 'value': 'Title'},
                            {'label': 'Artist', 'value': 'Artist'},
                            {'label': 'Lyrics', 'value': 'Lyrics'},
                            {'label': 'Liked', 'value': 'Liked'},
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
