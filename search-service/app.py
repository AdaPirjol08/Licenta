from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.config['YOUTUBE_API_KEY'] = 'YOUR_API_KEY_HERE'

@app.route('/search')
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={app.config['YOUTUBE_API_KEY']}"
    res = requests.get(url).json()
    videos = []
    for item in res.get("items", []):
        if 'videoId' in item['id']:
            videos.append({
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url']
            })
    return jsonify(videos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
