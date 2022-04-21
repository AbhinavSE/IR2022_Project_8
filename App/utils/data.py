import os
import pandas as pd
import json
from utils.caching import cache, TIMEOUT


@cache.memoize(timeout=TIMEOUT)
def load_music():
    music_df = pd.read_csv('assets/data/metadata.csv')
    music_df['image_folder'] = music_df['image_folder'].apply(lambda x: 'assets/data' + x if type(x) == str else x)
    # music = [
    #     {'artist': 'Gym Class Heroes', 'song': 'Stereo Hearts', 'album': 'Stereo Hearts', 'img': 'assets/album_covers/stereo_hearts.jpeg'},
    #     {'artist': 'Alan Walker', 'song': 'Faded', 'album': 'Faded', 'img': 'assets/album_covers/faded.jpg'},
    # ]
    # Repeat the above list to create a list of dictionaries
    return music_df.to_dict('records')


def get_likes():
    with open('tmp/likes.json') as f:
        likes = json.load(f)
        print('Got', likes)
        return likes


def set_likes(likes):
    print('Setting', likes)
    with open('tmp/likes.json', 'w') as f:
        json.dump(likes, f)
