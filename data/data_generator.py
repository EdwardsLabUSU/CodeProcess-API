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
        diff_cursor_pos = []
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
                diff_cursor_pos.append(len(code_book[:cursor_pos+1].split('\n')))
                event_book.append(row)
        return code_book, {'diff': diff_book, 'cursor_pos': diff_cursor_pos}



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
        grid_data, grid_points, diff_match_blocks, diff_line_number = DiffVisualizer.generate_grid_data(code, diff_book)
        DiffVisualizer.plot_grid(grid_data, code)
        return code, diff_book, grid_points, diff_match_blocks, diff_line_number
    
    @staticmethod
    def matching_lines(_final, _snap):
        def debug(s):
            #     print(s)
            pass

        class DiffHelper:
            def __init__(self, charjunk=None):
                self.charjunk = charjunk

            def _fancy_replace(self, abidx, a, alo, ahi, b, blo, bhi):
                r"""
            When replacing one block of lines with another, search the blocks
            for *similar* lines; the best-matching pair (if any) is used as a
            synch point, and intraline difference marking is done on the
            similar pair. Lots of work, but often worth it.
            Example:
            >>> d = Differ()
            >>> results = d._fancy_replace(['abcDefghiJkl\n'], 0, 1,
            ...                            ['abcdefGhijkl\n'], 0, 1)
            >>> print(''.join(results), end="")
            - abcDefghiJkl
            ?    ^  ^  ^
            + abcdefGhijkl
            ?    ^  ^  ^
            """

                # don't synch up unless the lines have a similarity score of at
                # least cutoff; best_ratio tracks the best score seen so far
                best_ratio, cutoff = 0.40, 0.55
                cruncher = difflib.SequenceMatcher(self.charjunk)
                eqi, eqj = None, None  # 1st indices of equal lines (if any)

                # search for the pair that matches best without being identical
                # (identical lines must be junk lines, & we don't want to synch up
                # on junk -- unless we have to)
                for j in range(blo, bhi):
                    bj = b[j]
                    cruncher.set_seq2(bj)
                    for i in range(alo, ahi):
                        ai = a[i]
                        if ai == bj:
                            if eqi is None:
                                eqi, eqj = i, j
                            continue
                        cruncher.set_seq1(ai)
                        # computing similarity is expensive, so use the quick
                        # upper bounds first -- have seen this speed up messy
                        # compares by a factor of 3.
                        # note that ratio() is only expensive to compute the first
                        # time it's called on a sequence pair; the expensive part
                        # of the computation is cached by cruncher
                        if cruncher.real_quick_ratio() > best_ratio and \
                                cruncher.quick_ratio() > best_ratio and \
                                cruncher.ratio() > best_ratio:
                            best_ratio, best_i, best_j = cruncher.ratio(), i, j
                if best_ratio < cutoff:
                    # no non-identical "pretty close" pair
                    if eqi is None:
                        # no identical pair either -- treat it as a straight replace
                        # TODO fix this
                        #                 debug('here')
                        #                 yield None
                        abidx[0] += sum([len(a[ali]) for ali in range(alo, ahi)])
                        abidx[1] += sum([len(b[bli]) for bli in range(blo, bhi)])
                        #                 abidx[1] += bhi-blo
                        #                 debug(' '.join(['xx', str(ahi), str(alo), str(bhi), str(blo)]))
                        #                 yield from self._plain_replace(a, alo, ahi, b, blo, bhi)
                        return
                    # no close pair, but an identical pair -- synch up on that
                    best_i, best_j, best_ratio = eqi, eqj, 1.0
                else:
                    # there's a close pair, so forget the identical pair (if any)
                    eqi = None

                # a[best_i] very similar to b[best_j]; eqi is None iff they're not
                # identical

                # pump out diffs from before the synch point
                debug('yy')
                yield from self._fancy_helper(abidx, a, alo, best_i, b, blo, best_j)

                # do intraline marking on the synch pair
                aelt, belt = a[best_i], b[best_j]
                #         debug('synch pair:', aelt, belt)
                if eqi is None:
                    # pump out a '-', '?', '+', '?' quad for the synched lines
                    atags = btags = ""
                    cruncher.set_seqs(aelt, belt)
                    debug('zz')
                    for tag, ai1, ai2, bj1, bj2 in cruncher.get_opcodes():
                        la, lb = ai2 - ai1, bj2 - bj1
                        #                 debug(' '.join(['zz', tag, a, b]))#a[abidx[0]], b[abidx[1]]]))
                        debug(' '.join(['zz', tag, str(abidx[0]), str(abidx[1]), str(la), str(lb)]))
                        #                 print(abidx)
                        if tag == 'replace':
                            atags += '^' * la
                            btags += '^' * lb
                            abidx[0] += la
                            abidx[1] += lb
                        elif tag == 'delete':
                            atags += '-' * la
                            abidx[0] += la
                        elif tag == 'insert':
                            btags += '+' * lb
                            abidx[1] += lb
                        elif tag == 'equal':
                            yield (abidx[0], abidx[1], la)
                            abidx[0] += la
                            abidx[1] += la
                            atags += ' ' * la
                            btags += ' ' * lb
                        else:
                            raise ValueError('unknown tag %r' % (tag,))
                #             yield from self._qformat(aelt, belt, atags, btags)
                else:
                    # the synch pair is identical
                    # TODO fix
                    debug('ww')
                    yield (abidx[0], abidx[1], len(aelt))
                #             yield '  ' + aelt

                # pump out diffs from after the synch point
                debug('gg')
                yield from self._fancy_helper(abidx, a, best_i + 1, ahi, b, best_j + 1, bhi)

            def _fancy_helper(self, abidx, a, alo, ahi, b, blo, bhi):
                g = []
                if alo < ahi:
                    debug('hh')
                    if blo < bhi:
                        #                 g = self._fancy_replace(abidx, a, alo, ahi, b, blo, bhi)
                        yield from self._fancy_replace(abidx, a, alo, ahi, b, blo, bhi)
                    else:
                        debug('ii')
                        #                 abidx[0] += ahi-alo
                        abidx[0] += sum([len(a[ali]) for ali in range(alo, ahi)])
                #                 abidx[1] += sum([len(b[bli]) for bli in range(blo, bhi)])

                #                 abidx[1] += bhi-blo
                #                 print('dump')
                #                 g = self._dump('-', a, alo, ahi)
                elif blo < bhi:
                    debug('jj')
                    #             abidx[0] += ahi-alo
                    #             abidx[1] += bhi-blo
                    #             abidx[0] += sum([len(a[ali]) for ali in range(alo, ahi)])
                    abidx[1] += sum([len(b[bli]) for bli in range(blo, bhi)])
            #             print('dump')
            #             g = self._dump('+', b, blo, bhi)

            #         yield from g

        def test(linejunk, a, b):
            blocks = []
            cruncher = difflib.SequenceMatcher(linejunk, a, b)
            ai = 0
            bi = 0
            helper = DiffHelper()
            for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
                astr = ''.join(a[alo:ahi])
                bstr = ''.join(b[blo:bhi])
                #         print(tag, alo, ahi, blo, bhi, astr, bstr)
                if tag == 'replace':
                    yield from helper._fancy_replace([ai, bi], a, alo, ahi, b, blo, bhi)
                    ai += len(astr)
                    bi += len(bstr)
                #             g = self._fancy_replace(a, alo, ahi, b, blo, bhi)
                elif tag == 'delete':
                    # in a
                    ai += len(astr)
                #             g = self._dump('-', a, alo, ahi)
                elif tag == 'insert':
                    # in b
                    bi += len(bstr)
                #             g = self._dump('+', b, blo, bhi)
                elif tag == 'equal':
                    #             blocks.append((ai, bi, len(astr)))
                    block = (ai, bi, len(astr))
                    ai += len(astr)
                    bi += len(astr)
                    yield block
                else:
                    raise ValueError('unknown tag %r' % (tag,))

            return blocks
        newline = True
        blocks = test(None, _final.splitlines(newline), _snap.splitlines(newline))
        return blocks

            # for b in blocks:
            #     print(b)
        # for b in blocks:
        #     print(b)
    
    @staticmethod
    def get_line_number(_code, char_pos, size):
        pre_highlight = _code[:char_pos + 1]
        post_highlight = _code[:char_pos + size+1]
        pre_line = pre_highlight.split('\n')
        post_line = post_highlight.split('\n')
        start_char = len(pre_line) - 1
        end_char = len(post_line) - 1
        return {
            'start_lne': len(pre_line),
            'start_char': start_char,
            'end_line': len(post_line),
            'end_char': end_char
        }
        
        

    @staticmethod
    def generate_grid_data(final_code, diff_list):
        
        
        def get_start_size(start, size, splitted):
            start_line = start
            end_line = start + size
            _start_index = len('\n'.join(splitted[:start_line]))
            _size = len('\n'.join(splitted[start_line:end_line + 1]))
            return _start_index, _size
        
        grid_data = []
        grid_points = []
        diff_match_blocks = []
        cursor_pos = diff_list['cursor_pos']
        diff_list = diff_list['diff']
        diff_line = []
        final_code_len = len(final_code)
        for row, each in enumerate(diff_list):
            # current_code = '\n'.join(each)
            then = datetime.datetime.now()
            current_code = each
            # d=difflib.SequenceMatcher(None, current_code, final_code)
            # d = difflib.SequenceMatcher(None, final_code, current_code)
            # mat = d.get_matching_blocks()
            # mat = DiffVisualizer.matching_lines(final_code, current_code)
            mat = DiffVisualizer.matching_lines(final_code, current_code)
            points = [0 for each in range(0, final_code_len)]
            # display(mat)
            match_block_diff = []
            match_block_final = []
            final_splitted = final_code.split('\n') 
            # for each_match in mat:
            #     start_index, size = get_start_size(each_match[0], each_match[2], final_splitted)
            #     
            #     # start_line = each_match[0]
            #     # end_line = each_match[0] + each_match[3]
            #     # startIndex = len(final_splitted[:start_line].join('\n'))
            #     # size = len(final_splitted[start_line:end_line+1].join('\n'))
            #     for i in range(start_index, start_index + size):
            #         points[i] = 1
            #         grid_points.append([i, row])
            #         
            #     current_start, current_size = get_start_size(each_match[1], each_match[2], splitted_snapshot)
            #     match_block_diff.append([current_start, current_size])
            #     match_block_final.append([start_index, size])

            for each_match in mat:
                initial_b = each_match[0]
                # initial_b = each_match.a
                size = each_match[2]
                # print('Initial b size: ', initial_b, size)
                for i in range(initial_b, initial_b + size):
                    points[i] = 1
                    grid_points.append([i, row])
                # match_block_diff.append([each_match[1], each_match[2]])
                # match_block_final.append([each_match[0], each_match[2]])
                match_block_diff.append(DiffVisualizer.get_line_number(current_code, each_match[1], each_match[2]))
                match_block_final.append(DiffVisualizer.get_line_number(final_code, each_match[0], each_match[2])),
            
                # match_block_diff.append([each_match.b, each_match.size])
                # match_block_final.append([each_match.a, each_match.size])
                
            
            # for each_match in mat[:-1]:
            #     initial_b = each_match.b
            #     # initial_b = each_match.a
            #     size = each_match.size
            #     # print('Initial b size: ', initial_b, size)
            #     for i in range(initial_b, initial_b + size):
            #         points[i] = 1
            #         grid_points.append([i, row])
            #     match_block_diff.append([each_match.a, each_match.size])
            #     match_block_final.append([each_match.b, each_match.size])
            #     # match_block_diff.append([each_match.b, each_match.size])
            #     # match_block_final.append([each_match.a, each_match.size])
            grid_data.append(points)
            # diff_match_blocks.append({
            #     'final': match_block_final,
            #     'snapShot': match_block_diff
            # })
            diff_match_blocks.append({
                'final': match_block_final,
                'snapShot': match_block_diff
            })
        grid_data.append([1 for _ in range(0, final_code_len)])
        return grid_data, grid_points, diff_match_blocks, diff_line

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
    import json, difflib
    dirs = [ name for name in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), name)) ]
    columns = ['event', 'input', 'removed', 'cursor_pos', 'timestamp', 'file', 'ver']
    print("Directories: ", dirs)
    for each_dir in dirs:
        if '__' in each_dir:
            continue
        path = os.path.join(os.getcwd(), each_dir)
        csv_file = pd.read_csv(os.path.join(path, 'phanonEditLog.csv'), names=columns, index_col=None)
        file_names = csv_file.file.unique()
        for each_name in file_names:
            print("Dir: ", each_dir, each_name)
            if each_name.split('.')[0] in each_dir or len(file_names) == 1:
                csv_file = csv_file[csv_file.file == each_name]
                code, diff_book, grid_data, diff_match_blocks, diff_line = DiffVisualizer.visualize(csv_file)

                diff_file = open(os.path.join(path, 'diff_book.csv'), 'w')
                json.dump(diff_book, diff_file)
                diff_file.close()

                code_file = open(os.path.join(path, 'code_book.txt'), 'w')
                code_file.writelines(code)
                code_file.close()

                grid_file = open(os.path.join(path, 'grid_point.json'), 'w')
                json.dump(grid_data, grid_file)
                grid_file.close()

                match_file = open(os.path.join(path, 'match_block.json'), 'w')
                json.dump(diff_match_blocks, match_file)
                match_file.close()

                diff_line_file = open(os.path.join(path, 'diff_line.json'), 'w')
                json.dump(diff_line, diff_line_file)
                diff_line_file.close()
