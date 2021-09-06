import os
import pandas as pd
from data.data_generator import DiffVisualizer
import gc, hashlib

OUTPUT_DIR = os.path.join(os.getcwd(), 'plots')

def list_dirs(current_dir):
    return sorted([name for name in os.listdir(current_dir) 
     if os.path.isdir(os.path.join(current_dir, name))])
    

if __name__ == '__main__':
    df_columns = ['event', 'input', 'removed', 'cursor_pos', 'timestamp', 'file', 'ver']
    search_dir = os.path.join(os.getcwd(), 'Future studies')
    dirs = list_dirs(search_dir)
    no_file = 0
    yes_file = 0
    for each_dir in dirs:
        current_dir = os.path.join(search_dir, each_dir)
        sub_dirs  = list_dirs(current_dir)
        for sub_dir in sub_dirs:
            phanon_dir = os.path.join(current_dir, sub_dir, '.idea', 'phanon', sub_dir, 'phanonEditLog.csv')
            if os.path.isfile(phanon_dir):
                csv_file = pd.read_csv(phanon_dir, names=df_columns, index_col=None)
                file_names = csv_file.file.unique()
                for each_file in file_names:
                    if not os.path.isfile(os.path.join(current_dir, sub_dir, each_file)):
                        continue
                    print(f"Working on: {each_dir} -> {sub_dir} -> {each_file}")
                    plot_name = os.path.join(OUTPUT_DIR, f"{each_dir}-{sub_dir}-({each_file}).jpeg")
                    if os.path.isfile(plot_name):
                        print("File exists....")
                        continue
                    elif ".py" not in each_file:
                        continue
                        
                    file_df = csv_file[csv_file.file == each_file]
                    code, diff_book, grid_data, diff_match_blocks, diff_line = DiffVisualizer.visualize(file_df, plot_name)
                    actual_code = open(os.path.join(current_dir, sub_dir, each_file), 'r')
                    ac_md5 = hashlib.md5()
                    ac_md5.update(actual_code.read().encode('utf-8'))
                    
                    f_md5 = hashlib.md5()
                    f_md5.update(code.encode('utf-8'))
                    
                    if f_md5.hexdigest() != ac_md5.hexdigest():
                        print("Generated code and actual code doesn't match... : ", f"{current_dir} -> {sub_dir} -> {each_file}")
                    actual_code.close()
                    del code
                    del diff_book
                    del diff_line
                    del grid_data
                    del diff_match_blocks
                    del file_df
                del csv_file
                yes_file += 1
            else:
                no_file += 1
        gc.collect()
    print("Total no file: ", no_file)
    print("Total yes file: ", yes_file)