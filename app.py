from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/search')
def search():
    q = request.args.get('q', '')
    if not q:
        return jsonify({'error': 'query required'}), 400
    
    opts = {
        'quiet': True,
        'extract_flat': True,
        'default_search': 'ytsearch10',
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f'ytsearch10:{q}', download=False)
    
    results = []
    for e in info.get('entries', []):
        results.append({
            'id': e.get('id'),
            'title': e.get('title'),
            'duration': e.get('duration'),
            'thumbnail': e.get('thumbnail'),
            'uploader': e.get('uploader'),
            'view_count': e.get('view_count'),
        })
    return jsonify(results)

@app.route('/api/stream')
def stream():
    vid_id = request.args.get('id', '')
    if not vid_id:
        return jsonify({'error': 'id required'}), 400
    
    opts = {
        'quiet': True,
        'format': 'best[ext=mp4]/best',
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(
            f'https://youtube.com/watch?v={vid_id}',
            download=False
        )
    
    return jsonify({
        'id': info.get('id'),
        'title': info.get('title'),
        'url': info.get('url'),
        'thumbnail': info.get('thumbnail'),
        'duration': info.get('duration'),
        'formats': [
            {
                'format_id': f.get('format_id'),
                'ext': f.get('ext'),
                'quality': f.get('quality'),
                'url': f.get('url'),
                'filesize': f.get('filesize'),
            }
            for f in info.get('formats', [])
            if f.get('url') and f.get('ext') in ['mp4', 'mp3', 'webm']
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'MongolStore Backend'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)