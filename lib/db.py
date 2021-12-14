import sqlite3

UPLOADED_FILES_COLUMNS = ("id", "uploaded_file_name", "url", "status", "message", "created_at")
PROCESSED_FILES_COLUMNS = ("id", "file_id", "file_name", "file_type", "url", "created_at")

def get_connection():
    conn = sqlite3.connect('database.db', check_same_thread=False)
    return conn


def db_setup():
    conn = get_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS uploaded_files (id text, uploaded_file_name TEXT, url TEXT, status TEXT, message TEXT, created_at TEXT);'
    )
    conn.execute(
        'CREATE TABLE IF NOT EXISTS processed_files (id  integer primary key autoincrement, file_id text, file_name TEXT, file_type TEXT, url TEXT, created_at TEXT);'
    )
    print("Creating table if does not exist....")
    conn.close()
