import os
import pandas as pd
import json
from utils.recommender import Recommender
from utils.VectorSearch import VectorSearch
from utils.searchAlgorithm import Search
from utils.caching import cache, TIMEOUT


@cache.memoize(timeout=TIMEOUT)
def load_music():
    music_df = pd.read_csv('assets/data/metadata.csv', encoding='latin1')
    music_df = music_df.fillna('')
    music_df['image_folder'] = music_df['image_folder'].apply(lambda x: 'assets/data' + x if type(x) == str else x)
    music_df['music_folder'] = music_df['music_folder'].apply(lambda x: 'assets/data' + x if type(x) == str else x)
    return music_df.to_dict('records')


@cache.memoize(timeout=TIMEOUT)
def getRecommender():
    return Recommender()


@cache.memoize(timeout=TIMEOUT)
def getSearchObject():
    return Search()


@cache.memoize(timeout=TIMEOUT)
def getLyricsSearchObject():
    return VectorSearch()


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
        return likes


def setLikes(likes):
    with open('tmp/likes.json', 'w') as f:
        json.dump(likes, f)
