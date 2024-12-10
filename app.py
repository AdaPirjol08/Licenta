from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)  # Store relative file path only

@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html', songs=songs, current_song=None)

@app.route('/add', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']
        file_path = request.form['file_path']

        # Save the file path as the filename (no full path)
        file_name = file_path.split('/')[-1]

        new_song = Song(title=title, artist=artist, genre=genre, file_path=file_name)
        db.session.add(new_song)
        db.session.commit()

        return redirect(url_for('index'))  # Redirect to the song list after adding a song

    return render_template('add_song.html')

@app.route('/play_song/<int:song_id>')
def play_song(song_id):
    song = Song.query.get_or_404(song_id)
    return render_template('index.html', songs=Song.query.all(), current_song=song)

@app.route('/delete_song/<int:song_id>', methods=['GET', 'POST'])
def delete_song(song_id):
    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('index'))  # Redirect to the song list after deletion

if __name__ == '__main__':
    app.run(debug=True, port=5001)
