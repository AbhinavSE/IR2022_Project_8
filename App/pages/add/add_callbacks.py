import base64
from utils.caching import cache
from utils.data import getSearchObject
from app import app
from dash.dependencies import Input, Output, State


@app.callback(
    [Output('add-song-alert', 'children'), Output('add-song-alert', 'color'), Output('add-song-alert', 'style')],
    [Input('add-song-button', 'n_clicks'), State('add-song-title', 'value'),
     State('add-song-artist', 'value'), State('add-song-mp3', 'contents'),
     State('add-song-mp3', 'filename')],
    prevent_initial_call=True
)
def addSongCallback(n_clicks, title, artist, contents, filename):
    if title is None or artist is None or contents is None:
        return 'Please fill out all fields', 'danger', {'display': 'block'}
    else:
        if 'mp3' not in filename.lower():
            return 'Please upload an MP3 file', 'danger', {'display': 'block'}
        else:
            print(title, artist)
            # Save the song in tmp/
            data = contents.encode('utf8').split(b';base64,')[1]
            song_path = 'assets/data/songs/' + filename
            with open(song_path, 'wb') as f:
                f.write(base64.b64decode(data))
            getSearchObject().addSongToDB([artist, title, f'/songs/{filename}'])
            cache.clear()

    return 'Song added successfully', 'success', {'display': 'block'}
