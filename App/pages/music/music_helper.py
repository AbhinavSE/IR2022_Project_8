from components.carousel import get_carousel

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
    