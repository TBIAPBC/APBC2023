import numpy as np
from func import *

opened_file = open('Manhattan-testHV3.in')

all_matrix = parse_file(opened_file)

simple = False
try:
    north_south, west_east = all_matrix
    simple = True
except ValueError as v:
    try:
        north_south, west_east, diag = all_matrix
        simple = False
    except Exception as e:
        print('Error when reading data!')
        exit()


[print(x) for x in north_south]
print('')
[print(x) for x in west_east]
print('')

arr = np.zeros((len(north_south)+1, len(north_south[0])))
arr = fill_matrix_easy(arr, north_south, west_east)

print(arr)

path = backtrace(arr, north_south, west_east)

print(path)





