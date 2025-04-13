from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    items = db.relationship("PlaylistItem", backref="playlist", lazy=True)

class PlaylistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlist.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    video_id = db.Column(db.String(50), nullable=False)
