from flask import Flask, render_template
from utils.api_client import get_users, get_songs, get_favorites

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/users')
def users():
    users = get_users()
    return render_template('users.html', users=users)

@app.route('/songs')
def songs():
    songs = get_songs()
    return render_template('songs.html', songs=songs)

@app.route('/favorites')
def favorites():
    favorites = get_favorites()
    return render_template('favorites.html', favorites=favorites)

if __name__ == '__main__':
    app.run(debug=True)