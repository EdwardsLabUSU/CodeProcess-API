import json
import os
import traceback
import uuid
import zipfile
from datetime import datetime

import pandas as pd

from .db import get_connection, UPLOADED_FILES_COLUMNS
from .phanon_visualizer import DiffVisualizer

"""
This function processes the pyphanon event log file and creates other necessary files needed by CodeProcess
Visualization software.
"""


def zip_file(unique_file_name, file_name, content, data_dir):
    _path = os.path.join(data_dir, f"{str(unique_file_name).split('.')[0]}.zip")
    print("Saved in: ", _path)
    zf = zipfile.ZipFile(_path, mode="w", compression=zipfile.ZIP_DEFLATED)
    zf.writestr(str(file_name), content)
    zf.close()
    return str(_path)


def process_file(file_id, data_dir):
    conn = get_connection()
    query = f'SELECT * FROM uploaded_files where status = "Uploaded" and id = "{file_id}";'
    df_columns = ['event', 'input', 'removed', 'cursor_pos', 'timestamp', 'file', 'ver']
    cur = conn.cursor()
    cur.execute(query)
    res = cur.fetchone()
    try:
        if res:
            row = dict(zip(UPLOADED_FILES_COLUMNS, res))
            print(row["url"])
            csv_file = pd.read_csv(row["url"], names=df_columns, index_col=None)
            file_names = csv_file.file.unique()
            for each_file in file_names:
                if ".py" not in str(each_file):
                    continue
                file_df = csv_file[csv_file.file == each_file]
                code, diff_book, grid_data, diff_match_blocks, diff_line = DiffVisualizer.visualize(file_df, data_dir)

                diff_book_file = uuid.uuid4()
                code_book_file = uuid.uuid4()
                grid_point_file = uuid.uuid4()
                match_block_file = uuid.uuid4()
                diff_line_file = uuid.uuid4()

                diff_book_url = zip_file(diff_book_file, "diff_book.csv", json.dumps(diff_book['diff']), data_dir)
                code_book_url = zip_file(code_book_file, "code_book.txt", code, data_dir)
                grid_point_url = zip_file(grid_point_file, "grid_point.json", json.dumps(grid_data), data_dir)
                match_block_url = zip_file(match_block_file, "match_block.json", json.dumps(diff_match_blocks),
                                           data_dir)
                diff_line_url = zip_file(diff_line_file, "diff_line.json", json.dumps(diff_line), data_dir)
                created_at = str(datetime.now())
                # Insert processed files and change the status to processed.
                query = "INSERT INTO processed_files (file_id, file_name, file_type, url, created_at) values (?, ?, ?, ?, ?);"
                print((
                    file_id, each_file, "diff_book.csv", diff_book_url, created_at
                ))
                cur.execute(query, (
                    file_id, each_file, "diff_book.csv", diff_book_url, created_at
                ))
                cur.execute(query, (
                    file_id, each_file, "code_book.txt", code_book_url, created_at
                ))
                cur.execute(query, (
                    file_id, each_file, "grid_point.json", grid_point_url, created_at
                ))
                cur.execute(query, (
                    file_id, each_file, "match_block.json", match_block_url, created_at
                ))
                cur.execute(query, (
                    file_id, each_file, "diff_line.json", diff_line_url, created_at
                ))
                update_query = f'UPDATE uploaded_files set status = "Processed", message="Success" where id = "{file_id}";'
                cur.execute(update_query)
                print("Success.....")
    except Exception as e:
        update_query = f'UPDATE uploaded_files set ' \
                       f'status = "Error", message="{e.args}" ' \
                       f'where id = "{file_id}";'
        cur.execute(update_query)
        print("Failed.....")
        traceback.print_exc()
    finally:
        conn.commit()
        conn.close()
