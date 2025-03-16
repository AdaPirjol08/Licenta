from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'ada_are_mere'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyA1XMpf0AEls3VkR8wA0ER7OxFEO64T5EA"

# -------------------- MODELS --------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    playlists = db.relationship("Playlist", backref="owner", lazy=True)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    items = db.relationship("PlaylistItem", backref="playlist", lazy=True)

class PlaylistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    video_id = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- ROUTES --------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/create_playlist', methods=['POST'])
@login_required
def create_playlist():
    name = request.form.get("playlist_name")
    if name:
        new_playlist = Playlist(name=name, user_id=current_user.id)
        db.session.add(new_playlist)
        db.session.commit()
        flash(f'Playlist "{name}" created!', "success")
    return redirect(url_for('index'))

@app.route('/')
@login_required
def index():
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    playlist_id = request.args.get("playlist_id")

    current_playlist = Playlist.query.get(playlist_id) if playlist_id else (playlists[0] if playlists else None)

    return render_template('index.html', playlists=playlists, current_playlist=current_playlist)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get("q")
    if not query:
        flash("Please enter a search term", "danger")
        return redirect(url_for("index"))

    videos = search_youtube(query)
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    playlist_id = request.args.get("playlist_id")
    current_playlist = Playlist.query.get(playlist_id) if playlist_id else (playlists[0] if playlists else None)

    return render_template("index.html", videos=videos, playlists=playlists, current_playlist=current_playlist)

def search_youtube(query):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}"
    response = requests.get(url).json()

    videos = []
    for item in response.get("items", []):
        video_id = item["id"].get("videoId")  # Extract correct video ID
        if not video_id:
            continue  # Skip if there's no video ID

        videos.append({
            "video_id": video_id,
            "title": item["snippet"]["title"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        })
    
    return videos

@app.route('/add_to_playlist', methods=['POST'])
@login_required
def add_to_playlist():
    title = request.form.get("title")
    video_id = request.form.get("video_id")
    playlist_id = request.form.get("playlist_id")

    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        flash("Playlist not found!", "danger")
        return redirect(url_for("index"))

    new_item = PlaylistItem(title=title, video_id=video_id, playlist=playlist)
    db.session.add(new_item)
    db.session.commit()

    flash("Added to playlist!", "success")
    return redirect(url_for("index"))

@app.route('/remove_from_playlist/<int:item_id>', methods=['POST'])
def remove_from_playlist(item_id):
    # Find the item and delete it
    item = PlaylistItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(request.referrer)  # Redirect back to the playlist

@app.route('/delete_playlist/<int:playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist:
        # Delete all songs associated with this playlist
        PlaylistItem.query.filter_by(playlist_id=playlist_id).delete()
        # Delete the playlist itself
        db.session.delete(playlist)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove_from_playlist/<int:item_id>')
@login_required
def remove_song(item_id):
    item = PlaylistItem.query.get_or_404(item_id)

    if item.playlist.owner.id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("index"))

    db.session.delete(item)
    db.session.commit()

    return redirect(url_for("index"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

