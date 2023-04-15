import numpy as np
from functions import *
import argparse

# Input is read from command line
parser = argparse.ArgumentParser()
parser.add_argument("input", help="file name")
parser.add_argument("-t", "--path", action="store_true", help="Returns one of the best paths.")
parser.add_argument("-d", "--diagonal", action="store_true", help="Diagonal reading are always available.")
args = parser.parse_args()
file_name = args.input
path_arg = args.path
diag_arg = args.diagonal

opened_file = open(file_name)

if diag_arg:
    print(f'My parser will always also read in files with diagonals. No flag "-d" needed.')
all_matrix = parse_file(opened_file)        # These are all the parsed matrices
arr = []                                    # This is the array we will fill with the best values

try:
    # If we have a 'simple' problem (no diagonal)
    north_south, west_east = all_matrix
    arr = np.zeros((len(north_south) + 1, len(north_south[0])))
    arr = fill_matrix_easy(arr, north_south, west_east)
    print(int(arr[-1][-1]))                                         # last entry in 'arr' is the best solution
    if path_arg:
        path = backtrace(arr, north_south, west_east)
        print(path)                                                 # this is the best path ('S' at multiple solutions)

except ValueError as v:

    try:
        # If we have a 'hard' problem (with diagonal)
        north_south, west_east, diag = all_matrix
        arr = np.zeros((len(north_south) + 1, len(north_south[0])))
        arr = fill_matrix_hard(arr, north_south, west_east, diag)
        print(round(arr[-1][-1], 2))                                # last entry in 'arr' is the best solution
        if path_arg:
            path = backtrace_hard(arr, north_south, west_east, diag)
            print(path)                                             # this is the best path ('S' at multiple solutions)

    except Exception as e:

        print('Error when reading data!')
        exit()
