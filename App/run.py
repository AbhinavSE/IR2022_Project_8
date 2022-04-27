from app import app
from routes import *
from layout import layout

server = app.server
app.layout = layout.layout

if __name__ == '__main__':
    app.run_server(debug=False)
