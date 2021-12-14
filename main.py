import os
import time
import uuid
import zipfile
from datetime import datetime
from io import BytesIO
from multiprocessing import Process

from flask import Flask, send_file, request, jsonify
from flask_compress import Compress
from flask_cors import CORS

from lib.db import get_connection, db_setup, UPLOADED_FILES_COLUMNS, PROCESSED_FILES_COLUMNS
from lib.process_file import process_file

app = Flask(__name__)
app.config['COMPRESS_ALGORITHM'] = 'gzip'
app.config['COMPRESS_LEVEL'] = 6
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['OUTPUT_FOLDER'] = './files'
CORS(app)
Compress(app)
path = os.getcwd()


def bad_request(message):
    return jsonify({
        "error": message
    }), 400


# First RUN CREATE tables if not exist.
db_setup()


def zip_file(file):
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        individualFile = file
        data = zipfile.ZipInfo(individualFile)
        data.date_time = time.localtime(time.time())[:6]
        data.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(data)
        # zf.writestr(data, individualFile['fileData'])
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='capsule.zip', as_attachment=True)


@app.route('/files')
def get_files():
    query = """SELECT uf.*, pf.file_name FROM uploaded_files uf inner join (
                    select distinct file_id, file_name from processed_files) pf on pf.file_id = uf.id
            WHERE uf.status = "Processed" order by uf.created_at desc
    """
    # 'where uf.status = "Processed" order by uf.created_at desc);'
    res = []
    _conn = get_connection()
    cur = _conn.cursor()
    columns = list(UPLOADED_FILES_COLUMNS)
    columns.append("file_name")
    for row in cur.execute(query):
        res.append(dict(zip(columns, row)))
    _conn.close()
    return jsonify({
        "data": {
            "rows": res
        }
    })


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return bad_request("No file uploaded")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return bad_request("No selected file")
        elif file and file.filename.split('.')[-1].lower() == 'csv':
            unique_id = str(uuid.uuid4())
            file_name = unique_id + " - " + file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            file.save(file_path)
            _conn = get_connection()
            data = (unique_id, file.filename, file_path, "Uploaded", "Waiting to be processed", str(datetime.now()))
            _conn.execute(
                "INSERT INTO uploaded_files (id, uploaded_file_name, url, status, message, created_at) values (?, ?, ?, ?, ?, ?);",
                data)
            _conn.commit()
            _conn.close()
            process = Process(  # Create a daemonic process with heavy "my_func"
                target=process_file,
                args=(unique_id, app.config["OUTPUT_FOLDER"]),
                daemon=True
            )
            process.start()
            return jsonify({
                "data": {
                    "message": f"Successfully uploaded.... ID: {unique_id}",
                    "id": unique_id
                }
            })
    return bad_request("Not allowed")


@app.route('/uploads/latest')
def get_latest_uploads():
    query = 'WITH sub as (' \
            'SELECT * FROM uploaded_files order by created_at desc LIMIT 15' \
            ')SELECT sub.*, COALESCE(sub2.count, 0) from sub left join (' \
            '   select count(*) as count, file_id from (SELECT distinct file_id, file_name from processed_files) group by file_id' \
            ') sub2 on sub2.file_id = sub.id;'
    res = []
    _conn = get_connection()
    cur = _conn.cursor()
    columns = list(UPLOADED_FILES_COLUMNS)
    columns.extend(['count'])
    for row in cur.execute(query):
        res.append(dict(zip(columns, row)))
    _conn.close()
    return jsonify({
        "data": {
            "rows": res
        }
    })


@app.route('/files/<file_id>')
def download_file(file_id):
    file = request.args.get('file_type')
    file_name = request.args.get('file_name')
    query = f"""
        SELECT * from processed_files where file_id = '{file_id}' and file_type = '{file}' and file_name = '{file_name}';
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    res = cur.fetchone()
    row = dict(zip(PROCESSED_FILES_COLUMNS, res))
    file_dir = os.path.join(app.config["OUTPUT_FOLDER"], row['url'])
    return send_file(file_dir)


@app.route('/data/<folder>/<file>')
def get_file(folder, file):
    file_dir = os.path.join(path, f"data/{folder}/{file}")
    # return zip_file(file_dir)
    return send_file(file_dir)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run("0.0.0.0", threaded=True, debug=True)

# git push heroku master
