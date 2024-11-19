from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        url = data['url']
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
