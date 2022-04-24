import re
from app import app
import dash
from dash import html
from dash.dependencies import Input, Output, State
from pages.music.music_helper import music_cards
from utils.data import get_likes, load_music, set_likes

# Like button callbacks


@app.callback(
    output=[Output(f'music-card-{i}-like-btn', 'children') for i in range(15)],
    inputs=dict(likes=[Input(f'music-card-{i}-like-btn', 'n_clicks') for i in range(15)]),
    state=dict(song_ids=[State(f'music-card-{i}-song-id', 'children') for i in range(15)]),
    prevent_initial_call=True,
)
def update_likes(likes, song_ids):
    """
    Updates the like button.
    """
    # Get the ctx trigger
    ctx = dash.callback_context
    # Get the button that was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id = re.search(r'\d+', button_id).group()
    song_id = song_ids[int(button_id)]
    likes_status = get_likes()
    if str(song_id) in likes_status:
        del likes_status[str(song_id)]
    else:
        likes_status[str(song_id)] = 1
    set_likes(likes_status)
    return ["❤️" if str(i) in likes_status else "🤍" for i in song_ids]


# Pagination callback
@app.callback(
    Output('music-cards', 'children'),
    [Input('music-pagination', 'active_page')],
)
def pagination(page):
    return music_cards(page, get_likes())

# Play selected music


@app.callback(
    output=Output('music-player', 'src'),
    inputs=dict(likes=[Input(f'music-card-{i}-play-btn', 'n_clicks') for i in range(15)]),
    state=dict(song_ids=[State(f'music-card-{i}-song-id', 'children') for i in range(15)]),
    prevent_initial_call=True,
)
def play_music(likes, song_ids):
    """
    Plays the selected music.
    """
    # Get the ctx trigger
    ctx = dash.callback_context
    # Get the button that was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id = re.search(r'\d+', button_id).group()
    song_id = song_ids[int(button_id)]
    music = load_music()
    print(music[song_id]['music_folder'])
    return music[song_id]['music_folder']
