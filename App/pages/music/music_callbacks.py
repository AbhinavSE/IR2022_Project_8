import re
from utils.data import getLyricsSearchObject
from app import app
import dash
from dash import html
from dash.dependencies import Input, Output, State
from pages.music.music_helper import getMusicCards, getRecommenedSongs
from utils.data import getLikes, load_music, setLikes, getSearchObject

# Like button callbacks


@app.callback(
    output=[Output(f'music-card-{i}-like-btn', 'children') for i in range(15)],
    inputs=dict(likes=[Input(f'music-card-{i}-like-btn', 'n_clicks') for i in range(15)]),
    state=dict(song_ids=[State(f'music-card-{i}-song-id', 'children') for i in range(15)]),
    prevent_initial_call=True,
)
def updateLikesCallback(likes, song_ids):
    """
    Updates the like button.
    """
    # Get the ctx trigger
    ctx = dash.callback_context
    # Get the button that was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_id = re.search(r'\d+', button_id).group()
    song_id = song_ids[int(button_id)]
    likes_status = getLikes()
    if str(song_id) in likes_status:
        del likes_status[str(song_id)]
    else:
        likes_status[str(song_id)] = 1
    setLikes(likes_status)
    return ["❤️" if str(i) in likes_status else "🤍" for i in song_ids]


# Pagination callback
@app.callback(
    [Output('music-pagination', 'max_value'), Output('music-cards', 'children')],
    [Input('music-pagination', 'active_page'),
     Input('music-search-text', 'value'), Input('music-search-type', 'value')],
)
def paginationCallback(page, text, search_type):
    music = load_music()
    text = text if text is not None else ''
    music = load_music()

    if search_type == 'Lyrics':
        if text != '':
            searchObj = getLyricsSearchObject()
            res = searchObj.searchSong(text)
            songs = res[1]
            music = [music[s] for s in songs]

    elif search_type == 'Liked':
        if text != '':
            searchObj = getSearchObject()
            res = searchObj.searchSong(text)
            songs = [r[0] for r in res if r[1] == 'Title']
            songs = [searchObj.map[r] for r in songs]
            music = [music[i] for s in songs for i in s]
        likes = list(getLikes().keys())
        music = [m for m in music if str(m['Id']) in likes]

    else:
        if text != '':
            searchObj = getSearchObject()
            res = searchObj.searchSong(text)
            songs = [r[0] for r in res if r[1] == search_type]
            songs = [searchObj.map[r] for r in songs]
            music = [music[i] for s in songs for i in s]

    totalPages = len(music) // 15 + 1
    pageSize = 15
    page = 1 if page is None else page - 1
    music = [music[i] for i in range(page * pageSize, min(len(music), (page + 1) * pageSize))]
    return totalPages, getMusicCards(music)


# Play selected music
@app.callback(
    output=[Output('music-player-audio', 'src'), Output('music-player-title', 'children'),
            Output('music-player-artist', 'children'), Output('music-player-cover-img', 'src')],
    inputs=dict(play_cards=[Input(f'music-card-{i}-play-btn', 'n_clicks') for i in range(15)], play_recom=Input('music-carousel-play-btn', 'n_clicks')),
    state=dict(song_ids=[State(f'music-card-{i}-song-id', 'children') for i in range(15)],
               carousel_items=State('music-carousel-slides', 'items'),
               carousel_ind=State('music-carousel-slides', 'active_index')),
    prevent_initial_call=True,
)
def playMusicCallback(play_cards, play_recom, song_ids, carousel_items, carousel_ind):
    """
    Plays the selected music.
    """
    # Get the ctx trigger
    ctx = dash.callback_context
    # Get the button that was clicked
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    audio, title, artist, cover = '', '', '', ''

    if button_id == 'music-carousel-play-btn':
        item = carousel_items[carousel_ind]
        song_id = int(item['id'])
    else:
        button_id = re.search(r'\d+', button_id).group()
        song_id = song_ids[int(button_id)]

    if song_id is not None:
        music = load_music()
        audio = music[song_id]['music_folder']
        title = music[song_id]['Title']
        artist = music[song_id]['Artist']
        cover = music[song_id]['image_folder']

    return [audio, title, artist, cover]


@app.callback(
    output=Output('music-carousel-slides', 'items'),
    inputs=dict(likes=[Input(f'music-card-{i}-like-btn', 'n_clicks') for i in range(15)]),
)
def recommendedSongsCarouselCallback(likes):
    """
    Carousel for the recommended songs.
    """
    items = getRecommenedSongs()
    for i in range(len(items)):
        items[i]['key'] = i + 1
    return items


@app.callback(
    output=[Output('music-carousel-title', 'children'), Output('music-carousel-artist', 'children')],
    inputs=[Input('music-carousel-slides', 'items'), Input('music-carousel-slides', 'active_index')],
)
def carouselTitleArtistCallback(items, active_index):
    """
    Carousel header for the recommended songs.
    """
    if active_index is None:
        active_index = 0
    title, artist = '', ''
    if active_index > -1 and active_index < len(items):
        title, artist = items[active_index]['title'], items[active_index]['artist']
    return title, artist
