import os
import pandas as pd


def load_music():
    music_df = pd.read_csv('assets/data/metadata.csv')
    music_df['image_folder'] = music_df['image_folder'].apply(lambda x: 'assets/data' + x if type(x) == str else x)
    print(music_df['image_folder'].iloc[0])
    # music = [
    #     {'artist': 'Gym Class Heroes', 'song': 'Stereo Hearts', 'album': 'Stereo Hearts', 'img': 'assets/album_covers/stereo_hearts.jpeg'},
    #     {'artist': 'Alan Walker', 'song': 'Faded', 'album': 'Faded', 'img': 'assets/album_covers/faded.jpg'},
    # ]
    # Repeat the above list to create a list of dictionaries
    return music_df.to_dict('records')[:20]
