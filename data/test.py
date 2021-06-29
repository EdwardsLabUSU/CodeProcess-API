import pandas as pd

from data.data_generator import DiffVisualizer

if __name__ == '__main__':
    file = '/home/pi/PycharmProjects/codeViz/data/LO1A2F01-U1-task#2-2/phanonEditLog.csv'
    columns = ['event', 'input', 'removed', 'cursor_pos', 'timestamp', 'file', 'ver']
    csv_file = pd.read_csv(file, names=columns, index_col=None)
    print("")
    _file = csv_file[csv_file.file === 'task2']
    code, diff_book, grid_data, diff_match_blocks, diff_line = DiffVisualizer.visualize(_file)
    
    
    