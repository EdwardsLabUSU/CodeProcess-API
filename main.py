import os, json

from flask import Flask, send_file
from flask_cors import CORS
from flask_compress import Compress
import gzip

app = Flask(__name__)
app.config['COMPRESS_ALGORITHM'] = 'gzip'
app.config['COMPRESS_LEVEL'] = 6
CORS(app)
Compress(app)
path = os.getcwd()



@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/data/<folder>/<file>')
def get_file(folder, file):
    file_dir = os.path.join(path, f"data/{folder}/{file}")
    return send_file(file_dir)

# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run("0.0.0.0", threaded=True)
