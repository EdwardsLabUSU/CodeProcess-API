import datetime
import difflib
import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np

event_book = []

DATA_DIR = '../data/'


class PhanonPlayback:

    @staticmethod
    def start_playback(data_frame):
        global event_book
        diff_book = []
        event_book = []
        code_book = ''
        for index, row in data_frame.iterrows():
            # print("Index: ", index)
            event = row['event']
            input = row['input']

            if event == 'e':
                cursor_pos = int(row['cursor_pos'])
                if not pd.isna(input):
                    # print(index, " -> ", cursor_pos, input)
                    code_book = code_book[:cursor_pos] + input + code_book[cursor_pos:]
                elif not pd.isna(row['cursor_pos']):
                    removed = row['removed']
                    if pd.isna(removed):
                        # print("Removed is also null here... : ", row)
                        continue
                    removed_length = len(removed)
                    if removed_length > 1:
                        code_book = code_book[:cursor_pos] + code_book[cursor_pos + len(removed):]
                        # code_book = code_book.replace(removed, '')
                    else:
                        code_book = code_book[:cursor_pos] + code_book[cursor_pos + 1:]
                else:
                    continue
                diff_book.append(code_book)
                event_book.append(row)
        return code_book, diff_book



EMPTY_CELL = 0
OBSTACLE_CELL = 1
START_CELL = 2
GOAL_CELL = 3
MOVE_CELL = 4
# create discrete colormap
cmap = colors.ListedColormap(['white','lightblue'])

class DiffVisualizer:

    @staticmethod
    def visualize(df):
        _df = df[(df.event == 'e') | (df.event == 'a')]
        code, diff_book = PhanonPlayback.start_playback(_df)
        grid_data, grid_points = DiffVisualizer.generate_grid_data(code, diff_book)
        DiffVisualizer.plot_grid(grid_data, code)
        return code, diff_book, grid_points

    @staticmethod
    def generate_grid_data(final_code, diff_list):
        grid_data = []
        grid_points = []
        final_code_len = len(final_code)
        for row, each in enumerate(diff_list):
            # current_code = '\n'.join(each)
            then = datetime.datetime.now()
            current_code = each
            # d=difflib.SequenceMatcher(None, current_code, final_code)
            d = difflib.SequenceMatcher(None, final_code, current_code)
            mat = d.get_matching_blocks()
            points = [0 for each in range(0, final_code_len)]
            # display(mat)
            for each_match in mat[:-1]:
                initial_b = each_match.a
                # initial_b = each_match.b
                size = each_match.size
                # print('Initial b size: ', initial_b, size)
                for i in range(initial_b, initial_b + size):
                    points[i] = 1
                    grid_points.append([i, row])
            grid_data.append(points)
        grid_data.append([1 for _ in range(0, final_code_len)])
        return grid_data, grid_points

    @staticmethod
    def plot_grid(data, final_code):

        fig, ax = plt.subplots(figsize=(25, 8))
        ax.set_aspect('auto')
        ax.imshow(data, cmap=cmap, aspect='auto')
        # draw gridlines
        events = len(data)
        x_major_ticks = np.arange(0, len(final_code), 100)
        x_minor_ticks = np.arange(0, len(final_code), 50)

        y_major_ticks = np.arange(0, events, 100)
        y_minor_ticks = np.arange(0, events, 50)

        ax.set_xticks(x_major_ticks)
        ax.set_xticks(x_minor_ticks, minor=True)

        ax.set_yticks(y_major_ticks)
        ax.set_yticks(y_minor_ticks, minor=True)

        ax.grid(which='both')
        ax.grid(which='major', color='#CCCCCC', linestyle='-', lw=0.7, alpha=0.5)
        ax.grid(which='minor', color='#CCCCCC', linestyle='-', lw=0.7, alpha=0.5)
        plt.show()


if __name__ == '__main__':
    import json
    dirs = [ name for name in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), name)) ]
    columns = ['event', 'input', 'removed', 'cursor_pos', 'timestamp', 'file', 'ver']
    print("Directories: ", dirs)
    for each_dir in dirs:
        path = os.path.join(os.getcwd(), each_dir)
        csv_file = pd.read_csv(os.path.join(path, 'phanonEditLog.csv'), names=columns, index_col=None)
        file_names = csv_file.file.unique()
        for each_name in file_names:
            print("Dir: ", each_dir, each_name)
            if each_name.split('.')[0] in each_dir or len(file_names) == 1:
                csv_file = csv_file[csv_file.file == each_name]
                code, diff_book, grid_data = DiffVisualizer.visualize(csv_file)

                diff_file = open(os.path.join(path, 'diff_book.csv'), 'w')
                json.dump(diff_book, diff_file)
                diff_file.close()

                code_file = open(os.path.join(path, 'code_book.txt'), 'w')
                code_file.writelines(code)
                code_file.close()

                grid_file = open(os.path.join(path, 'grid_point.json'), 'w')
                json.dump(grid_data, grid_file)
                grid_file.close()
