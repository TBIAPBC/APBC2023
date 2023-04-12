import numpy as np
import re
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="enter input filename")
    args = parser.parse_args()
    inputfile = args.input


# function to read the file
def read_matrix(input):
    i = 0
    distances = []
    with open(input, "r") as content:
        for line in content:
            i += 1
            # the first line contains the number of capitals and the limit
            if i == 1:
                ncap, limit = line.split()
            # the second line contains the city names
            if i == 2:
                capitals = line.split()
            # all the other lines contain the elements of the distance matrix
            # the list distances is filled with lists to create an array
            if i > 2:
                val = line.split()
                val = [re.sub("-", "0", x) for x in val]
                val = [int(x) for x in val]
                distances.append(val)
            inp_matrix = np.array([np.array(xi) for xi in distances])

    # the city names are made accessible by a number depending on their position in the matrix
    i = 0
    city_dict = {}
    for city in capitals:
        city_dict[str(i)] = city
        i += 1
    return inp_matrix, city_dict, ncap, limit, capitals


def function(matrix, dict, max_limit):
    score = 0
    cities_list = []
    visited_cities = []
    i = 0
    it = np.nditer(matrix, flags=["multi_index"], op_flags=["readwrite"])
    for x in it:
        i += 1
        print(i)
        if x > 0:
            var = score + x
            if var <= max_limit:
                cities_list.append(dict[str(it.multi_index[0])] + dict[str(it.multi_index[1])])
                matrix_new = np.delete(matrix, it.multi_index[0], 0)
                matrix_new = np.delete(matrix_new, it.multi_index[1], 1)
                if matrix_new.size == 0:
                    print(cities_list)
                    return cities_list, var
                else:
                    return function(matrix_new, dict, max_limit)
            else:
                continue
        else:
            # if it.multi_index[0] == it.multi_index[1]:
            continue


inp_matrix, city_dict, ncap, limit, capitals = read_matrix(inputfile)
function(inp_matrix, city_dict, limit)
output = "gobjul_test.out"

