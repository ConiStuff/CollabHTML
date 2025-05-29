from flask import Flask, request, send_from_directory, jsonify
import os
import re

app = Flask(__name__)
COLLAB_FILE = os.path.join('server', 'collab.html')
BANNED_WORDS = ['badword1', 'badword2']  

def filter_content(html):
    html = re.sub(r'(?is)<script.*?>.*?</script>', '', html)
    for word in BANNED_WORDS:
        html = html.replace(word, '[filtered]')
    return html

@app.route('/collab-source', methods=['GET'])
def get_collab_source():
    try:
        with open(COLLAB_FILE, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception:
        return 'Could not read file', 500

@app.route('/collab-source', methods=['POST'])
def post_collab_source():
    try:
        html = request.data.decode('utf-8')
        filtered = filter_content(html)
        with open(COLLAB_FILE, 'w', encoding='utf-8') as f:
            f.write(filtered)
        return '', 200
    except Exception:
        return 'Could not write file', 500

@app.route('/server/<path:filename>')
def serve_collab_html(filename):
    return send_from_directory('server', filename)

if __name__ == '__main__':
    os.makedirs('server', exist_ok=True)
    if not os.path.exists(COLLAB_FILE):
        with open(COLLAB_FILE, 'w', encoding='utf-8') as f:
            f.write('<h1>Welcome to CollabHTML!</h1>')
    app.run(host='0.0.0.0', port=8080, debug=True)
