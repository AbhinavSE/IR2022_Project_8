import os
import pandas as pd
import json
from utils.searchAlgorithm import Search
from utils.caching import cache, TIMEOUT


@cache.memoize(timeout=TIMEOUT)
def load_music():
    music_df = pd.read_csv('assets/data/metadata.csv', encoding='latin1')
    music_df = music_df.fillna('')
    music_df['image_folder'] = music_df['image_folder'].apply(lambda x: 'assets/data' + x if type(x) == str else x)
    music_df['music_folder'] = music_df['music_folder'].apply(lambda x: 'assets/data' + x if type(x) == str else x)
    # music = [
    #     {'artist': 'Gym Class Heroes', 'song': 'Stereo Hearts', 'album': 'Stereo Hearts', 'img': 'assets/album_covers/stereo_hearts.jpeg'},
    #     {'artist': 'Alan Walker', 'song': 'Faded', 'album': 'Faded', 'img': 'assets/album_covers/faded.jpg'},
    # ]
    # Repeat the above list to create a list of dictionaries
    return music_df.to_dict('records')


@cache.memoize(timeout=TIMEOUT)
def getSearchObject():
    search = Search()
    return search


def isSongLiked(songID):
    likedSongs = getLikes()
    if type(songID) == str:
        return str(songID) in likedSongs
    elif isinstance(songID, (list, tuple, set)):
        return [str(s) in likedSongs for s in songID]
    else:
        print(f'Invalid Type argument: {type(songID)}')


def getLikes():
    with open('tmp/likes.json') as f:
        likes = json.load(f)
        print('Got', likes)
        return likes


def setLikes(likes):
    print('Setting', likes)
    with open('tmp/likes.json', 'w') as f:
        json.dump(likes, f)
