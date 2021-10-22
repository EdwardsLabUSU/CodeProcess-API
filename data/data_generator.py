import os

import numpy as np
import pandas as pd
from matplotlib import colors
from matplotlib import pyplot as plt
import pickle, random, string

from lib.diff import get_diff_blocks

event_book = []

DATA_DIR = '/home/pi/PycharmProjects/codeViz/data'

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# class PhanonPlayback:
# 
#     @staticmethod
#     def start_playback(data_frame):
#         print("Hello panda...")
#         global event_book
#         diff_book = []
#         event_book = []
#         code_book = ''
#         pre_action = None
#         output_file = open(os.path.join(DATA_DIR, 'output.txt'), 'w')
#         for index, row in data_frame.iterrows():
#             # print("Index: ", index)
#             event = row['event']
#             input = row['input']
#             removed = row['removed']
# 
#             if event == 'e':
#                 cursor_pos = int(row['cursor_pos'])
#                 if len(input) > 0:
#                     code_book = code_book[:cursor_pos] + input + code_book[cursor_pos:]
#                 # elif len(removed) > 0:
#                 #     
#                 # if not pd.isna(input):
#                 #     # print(index, " -> ", cursor_pos, input)
#                     
#                 elif not pd.isna(row['cursor_pos']):
#                     
#                     if pd.isna(removed):
#                         # print("Removed is also null here... : ", row)
#                         pass
#                     else:
#                         removed_length = len(removed)
#                         if removed_length >= 1:
#                             code_book = code_book[:cursor_pos] + code_book[cursor_pos + len(removed):]
#                             # code_book = code_book.replace(removed, '')
#                         else:
#                             code_book = code_book[:cursor_pos] + code_book[cursor_pos + 1:]
#                 else:
#                     pass
#                 pre_action = None
#                 # elif event == 'a':
#                 #   if input and  pre_action:
#                 #     if pre_action == 'Select All' and input == 'Delete':
#                 #       pre_action = 'Delete All'
#                 #   else:
#                 #     pre_action = input
# 
#                 output_file.write('###########################################################')
#                 output_file.write(
#                     str(index) + '-' + "Removed: " + str(len(row['removed'])) if not pd.isna(row['removed']) else '0')
#                 output_file.write('\n' + str(row) + '\n')
# 
#                 output_file.write("************************************************\n")
#                 output_file.write(code_book)
#                 output_file.write("************************************************\n")
#                 # print('---------------')
#                 # print("Code: ", code_book)
#                 # print('---------------')
#                 diff_book.append(code_book)
#                 event_book.append(row)
# 
#             # print(row['event'], row['input'])
#         output_file.close()
#         return code_book, {'diff': diff_book, 'cursor_pos': []}

# 
class PhanonPlayback:

    @staticmethod
    def start_playback(data_frame):
        global event_book
        diff_book = []
        event_book = []
        diff_cursor_pos = []
        code_book = ''
        output_file = open(os.path.join(DATA_DIR, 'output.txt'), 'w')
        for index, row in data_frame.iterrows():
            # print("Index: ", index)
            event = row['event']
            input = row['input']
            cursor = row['cursor_pos']
            removed = row['removed']
            if event == 'e':
                if not pd.isna(cursor):
                    cursor_pos = int(cursor)
                    if not pd.isna(input) and len(input) > 0:
                        code_book = code_book[:cursor_pos] + input + code_book[cursor_pos:]
                    elif not pd.isna(removed) and len(removed) > 0:
                        code_book = code_book[:cursor_pos] + code_book[cursor_pos + len(removed):]
                # if not pd.isna(input):
                    # print(index, " -> ", cursor_pos, input)
                    # code_book = code_book[:cursor_pos] + input + code_book[cursor_pos:]
                # elif not pd.isna(row['cursor_pos']):
                #     removed = row['removed']
                #     if pd.isna(removed):
                #         # print("Removed is also null here... : ", row)
                #         continue
                #     removed_length = len(removed)
                #     if removed_length >= 1:
                #         code_book = code_book[:cursor_pos] + code_book[cursor_pos + len(removed):]
                #         # code_book = code_book.replace(removed, '')
                #     else:
                #         code_book = code_book[:cursor_pos] + code_book[cursor_pos + 1:]

                    output_file.write('###########################################################\n')
                    output_file.write(
                        str(index) + '-' + "Removed: " + str(len(row['removed'])) if not pd.isna(row['removed']) else '0')
                    output_file.write(
                        str(index) + '-' + "Input: " + str(len(row['input'])) if not pd.isna(row['input']) else '0')
                    output_file.write('\n' + str(row) + '\n')
                    output_file.write("************************************************\n")
                    output_file.write(code_book)
                    output_file.write("************************************************\n")
                    diff_book.append(code_book)
                    diff_cursor_pos.append(len(code_book[:cursor_pos + 1].split('\n')))
                    event_book.append(row)
        output_file.close()
        return code_book, {'diff': diff_book, 'cursor_pos': diff_cursor_pos}


EMPTY_CELL = 0
OBSTACLE_CELL = 1
START_CELL = 2
GOAL_CELL = 3
MOVE_CELL = 4
# create discrete colormap
cmap = colors.ListedColormap(['white', 'lightblue'])


class DiffVisualizer:

    @staticmethod
    def visualize(df, *args, **kwargs):
        _df = df[(df.event == 'e') | (df.event == 'a')]
        code, diff_book = PhanonPlayback.start_playback(_df)
        grid_data, grid_points, diff_match_blocks, diff_line_number = DiffVisualizer.generate_grid_data(code, diff_book)
        DiffVisualizer.plot_grid(grid_data, code, *args, **kwargs)
        # code:  contains the final code
        # diff_book: contains the snapshot of the current code for each event.
        # grid_points: contains the points required to plot the visualization.
        # diff_match_blocks: contains the matching parameters between the snapshot and final code.. 
        #                       ->  Used to highlight the common portion on the code. 
        # diff_line_number: contains the line number of a cursor for each code snapShot. 
        return code, diff_book, grid_points, diff_match_blocks, diff_line_number

    @staticmethod
    def matching_lines(_final, _snap):
        return get_diff_blocks(_final, _snap)

    @staticmethod
    def get_line_number(_code, char_pos, size):
        pre_highlight = _code[:char_pos + 1]
        post_highlight = _code[:char_pos + size + 1]
        pre_line = pre_highlight.split('\n')
        post_line = post_highlight.split('\n')
        start_char = len(pre_line[-1]) - 1
        end_char = len(post_line[-1]) - 1
        return {
            'start_line': len(pre_line),
            'start_char': start_char,
            'end_line': len(post_line),
            'end_char': end_char
        }

    @staticmethod
    def generate_grid_data(final_code, diff_list):

        grid_data = []
        grid_points = []
        diff_match_blocks = []

        cursor_positions = diff_list['cursor_pos']
        diff_list = diff_list['diff']

        final_code_len = len(final_code)
        for row, each in enumerate(diff_list):
            current_code = each
            mat = DiffVisualizer.matching_lines(final_code, current_code)
            points = [0 for _ in range(0, final_code_len)]
            match_block_diff = []
            match_block_final = []

            for each_match in mat:
                initial_b = each_match[0]
                size = each_match[2]
                for i in range(initial_b, initial_b + size):
                    points[i] = 1
                    grid_points.append([i, row])

                match_block_diff.append(DiffVisualizer.get_line_number(current_code, each_match[1], each_match[2]))
                match_block_final.append(DiffVisualizer.get_line_number(final_code, each_match[0], each_match[2])),

            grid_data.append(points)
            diff_match_blocks.append({
                'final': match_block_final,
                'snapShot': match_block_diff
            })
        grid_data.append([1 for _ in range(0, final_code_len)])
        return grid_data, grid_points, diff_match_blocks, cursor_positions

    @staticmethod
    def plot_grid(data, final_code, plot_dir=None, pickle_dir = None, identifier = None):

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
        if plot_dir:
            plt.savefig(os.path.join(plot_dir, f"{identifier}.png"))
        if pickle_dir:
            pickle_data = {
                'data': data,
                'y_ticks': {
                    'major': y_major_ticks,
                    'minor': y_minor_ticks
                },
                'x_ticks': {
                    'major': x_major_ticks,
                    'minor': y_minor_ticks
                },
                'final_code': final_code
            }
            with open(os.path.join(pickle_dir, f'{identifier} .pickle'), 'wb') as handle:
                pickle.dump(pickle_data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
        # plt.show()
        # plt.close()
#         


if __name__ == '__main__':
    import json

    dirs = [name for name in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), name))]
    columns = ['event', 'input', 'removed', 'cursor_pos', 'timestamp', 'file', 'ver']
    # print("Directories: ", dirs)
    # dirs = ['LO1A7M08-TG-Unit7-main']
    for each_dir in dirs:
        if '__' in each_dir:
            continue
        path = os.path.join(os.getcwd(), each_dir)
        csv_file = pd.read_csv(os.path.join(path, 'phanonEditLog.csv'), names=columns, index_col=None)
        file_names = csv_file.file.unique()
        print(csv_file.head())
        print("File names: ", file_names)
        for each_name in file_names:
            if '.'.join(each_name.split('.')[:-1]) in each_dir or len(file_names) == 1:
                if ".py" not in each_name:
                    print("Continued...")
                    continue
                _file_df = csv_file[csv_file.file == each_name]
                print("Dir: ", each_dir, each_name, _file_df.shape)
                code, diff_book, grid_data, diff_match_blocks, diff_line = DiffVisualizer.visualize(_file_df)
                
                
                
                import zipfile
                
                def zip_file(file_name, content):
                    _path = os.path.join(path, f"{file_name.split('.')[0]}.zip")
                    zf = zipfile.ZipFile(_path, mode="w", compression=zipfile.ZIP_DEFLATED)
                    zf.writestr(file_name, content)
                    zf.close()
                
                # diff_file = open(os.path.join(path, 'diff_book.csv'), 'w')
                # json.dump(diff_book['diff'], diff_file)
                # diff_file.close(os.path.join(path, 'diff_book.csv'))
                
                zip_file("diff_book.csv", json.dumps(diff_book['diff']))
                zip_file('code_book.txt', code)
                zip_file('grid_point.json', json.dumps(grid_data))
                zip_file('match_block.json', json.dumps(diff_match_blocks))
                zip_file('diff_line.json', json.dumps(diff_line))
                

                # code_file = open(os.path.join(path, 'code_book.txt'), 'w')
                # code_file.writelines(code)
                # code_file.close()
                # 
                # grid_file = open(os.path.join(path, 'grid_point.json'), 'w')
                # json.dump(grid_data, grid_file)
                # grid_file.close()
                # 
                # match_file = open(os.path.join(path, 'match_block.json'), 'w')
                # json.dump(diff_match_blocks, match_file)
                # match_file.close()
                # 
                # diff_line_file = open(os.path.join(path, 'diff_line.json'), 'w')
                # json.dump(diff_line, diff_line_file)
                # diff_line_file.close()
