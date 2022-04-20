import pandas as pd


def load_music():
    # music_df = pd.read_csv('assets/data/music.csv')
    music = [
        {'artist': 'Gym Class Heroes', 'song': 'Stereo Hearts', 'album': 'Stereo Hearts', 'img': 'assets/album_covers/stereo_hearts.jpeg'},
        {'artist': 'Alan Walker', 'song': 'Faded', 'album': 'Faded', 'img': 'assets/album_covers/faded.jpg'},
    ]
    # Repeat the above list to create a list of dictionaries
    music = music * 5
    return music
