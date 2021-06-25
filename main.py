import os, json

from flask import Flask, make_response
from flask_cors import CORS
import gzip

app = Flask(__name__)
CORS(app)
path = os.getcwd()



@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


@app.route('/data/<folder>/<file>')
def get_file(folder, file):
    file_dir = os.path.join(path, f"data/{folder}/{file}")
    content = gzip.compress(json.dumps(open(file_dir, 'r').readlines()).encode('utf8'), 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    return response


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run("0.0.0.0", threaded=True)
