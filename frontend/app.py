#from flask import Flask, render_template, request, redirect, url_for, flash
import requests 
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import session  

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "frontend_secret"

AUTH_URL = "http://auth-service:5001"
PLAYLIST_URL = "http://playlist-service:5002"
SEARCH_URL = "http://search-service:5003"

@app.route('/')
@app.route('/playlist/<int:playlist_id>')
def home(playlist_id=None):
    user_id = session.get("user_id")
    
    try:
        playlists = requests.get(f"{PLAYLIST_URL}/playlists/{user_id}").json()
    except:
        playlists = []

    current = next((pl for pl in playlists if str(pl["id"]) == str(playlist_id)), playlists[0] if playlists else None)

    # Nou: încarcă itemele din playlist curent
    items = []
    if current:
        try:
            items = requests.get(f"{PLAYLIST_URL}/playlists/{current['id']}/items").json()
        except:
            items = []
    user_id = session.get("user_id")
    user_tier = session.get("tier", "free")
    
    return render_template(
    "index.html",
    playlists=playlists,
    current_playlist=current,
    videos=[],
    items=items,
    tier=user_tier
)


@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    try:
        title = request.form.get("title")
        video_id = request.form.get("video_id")
        playlist_id = request.form.get("playlist_id")

        if not all([title, video_id, playlist_id]):
            flash("Invalid form data", "danger")
            return redirect("/")

        requests.post(f"{PLAYLIST_URL}/playlists/{playlist_id}/items", json={
            "title": title,
            "video_id": video_id
        })

    except Exception as e:
        print("❌ Error adding to playlist:", e)
        flash("Failed to add video to playlist.", "danger")

    return redirect("/")



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tier = request.form.get('tier', 'free')  # default to free

        r = requests.post(f"{AUTH_URL}/register", json={
            "username": username,
            "password": password,
            "tier": tier
        })

        if r.status_code == 201:
            flash("Registered!", "success")
            return redirect("/login")
        else:
            flash("Username already exists.", "danger")

    return render_template("register.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        r = requests.post(f"{AUTH_URL}/login", json={"username": username, "password": password})

        if r.status_code == 200:
            data = r.json()
            session["user_id"] = data["user_id"]
            session["tier"] = data["tier"]
            flash("Logged in!", "success")
            return redirect('/')
        flash("Login failed", "danger")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect("/login")



@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    name = request.form.get("playlist_name")
    user_id = session.get("user_id")

    requests.post(f"{PLAYLIST_URL}/playlists", json={"name": name, "user_id": user_id})
    return redirect("/")

@app.route('/delete_playlist/<int:playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    requests.delete(f"{PLAYLIST_URL}/playlists/{playlist_id}")
    return redirect("/")

@app.route('/search')
def search():
    query = request.args.get("q")
    if not query:
        flash("Please enter a search term", "danger")
        return redirect('/')
    videos = requests.get(f"{SEARCH_URL}/search", params={"q": query}).json()
    user_id = session.get("user_id")

    playlists = requests.get(f"{PLAYLIST_URL}/playlists/{user_id}").json()
    current_playlist = playlists[0] if playlists else None
    return render_template("index.html", playlists=playlists, current_playlist=current_playlist, videos=videos)


@app.route('/remove_from_playlist/<int:item_id>', methods=['POST'])
def remove_from_playlist(item_id):
    requests.delete(f"{PLAYLIST_URL}/items/{item_id}")
    return redirect('/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
