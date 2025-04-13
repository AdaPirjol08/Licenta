from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playlists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELE
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    items = db.relationship('PlaylistItem', backref='playlist', cascade='all, delete-orphan')

class PlaylistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    video_id = db.Column(db.String(100))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))

# ENDPOINTS
@app.route('/playlists/<int:user_id>', methods=['GET'])
def get_playlists(user_id):
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"id": pl.id, "name": pl.name, "user_id": pl.user_id} for pl in playlists
    ])

@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.get_json()
    new_playlist = Playlist(name=data['name'], user_id=data['user_id'])
    db.session.add(new_playlist)
    db.session.commit()
    return jsonify({"message": "Playlist created", "id": new_playlist.id}), 200

@app.route('/playlists/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        return jsonify({"message": "Playlist deleted"}), 200
    return jsonify({"error": "Playlist not found"}), 404

@app.route('/playlists/<int:playlist_id>/items', methods=['POST'])
def add_item_to_playlist(playlist_id):
    data = request.get_json()
    print("🎵 Received data:", data)
    new_item = PlaylistItem(
        playlist_id=playlist_id,
        title=data['title'],
        video_id=data['video_id']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Item added"}), 200

@app.route('/playlists/<int:playlist_id>/items', methods=['GET'])
def get_playlist_items(playlist_id):
    items = PlaylistItem.query.filter_by(playlist_id=playlist_id).all()
    return jsonify([
        {"id": item.id, "title": item.title, "video_id": item.video_id}
        for item in items
    ])

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = PlaylistItem.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed"}), 200
    return jsonify({"error": "Item not found"}), 404

# RUN
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002)
