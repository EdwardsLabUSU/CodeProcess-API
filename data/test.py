from data_generator import DiffVisualizer
final ='''# CS 1XXX 
# Assignment 1 First Program
# Mr. Legitimate work 

import random
sortlist = random.sample(range(0, 40), 10)
print("unsorted list")
print(sortlist)

print ("sorting list...")
for i in range(0, len(sortlist)):
    # print(sortlist[i])
    for j in range(0, len(sortlist)):
        if sortlist[i] > sortlist[j]:
            temp = sortlist[i]
            sortlist[i] = sortlist[j]
            sortlist[j] = temp
print("finished sorting")
print("sorted list")
print(sortlist)
'''

snapShot = '''# CS 1XX


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
'''
grid_data, grid_points, diff_match_blocks = DiffVisualizer.generate_grid_data(final, [snapShot])
print(grid_data)
print(grid_points)
print(diff_match_blocks)