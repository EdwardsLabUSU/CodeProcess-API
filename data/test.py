import pandas as pd
import os

from data.data_generator import DiffVisualizer

if __name__ == '__main__':
    # file = '/home/pi/PycharmProjects/codeViz/data/LO1A2F01-U1-task#2-2/phanonEditLog.csv'
    # columns = ['event', 'input', 'removed', 'cursor_pos', 'timestamp', 'file', 'ver']
    # csv_file = pd.read_csv(file, names=columns, index_col=None)
    # print(csv_file.file.unique())
    # _file = csv_file[csv_file.file == 'task#2-2.py']
    # code, diff_book, grid_data, diff_match_blocks, diff_line = DiffVisualizer.visualize(_file)
    # print(code)
    dirs = [name for name in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), name))]
    for each in dirs:
        print(f'<option value="{each}">{each.replace("-", " ")}</option>')
    print(dirs)
    
    
    