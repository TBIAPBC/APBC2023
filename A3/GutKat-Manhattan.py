import argparse
import numpy as np
from math import ceil

# get the arguments
parser = argparse.ArgumentParser(description='A3 - The Manhattan Tourist Problem')
parser.add_argument('input', type=str, help='the input file')
parser.add_argument('-t', action='store_true', help='print best path through grid')
parser.add_argument('-d', action='store_true', help='include diagonal streets')
args = parser.parse_args()

edges = []
with open(args.input, "r") as f:
    for line in f:
        # only get line if it does not start with # and is not an empty line (\n)
        if not line.startswith("#") and line != "\n":
            line = line.replace("\n", "").split(" ")
            # get every number within the line
            edges.append([round(float(x),2) for x in line if x])

# if we use diagonal, also get the diagonal lines
if args.d:
    n = ceil(len(edges)/3)
    horizontals = edges[0:n-1]
    verticals = edges[n-1:(2*n-1)]
    diagonals = edges[(2*n-1):]
    #convert edge weights into np array
    horizontals = np.array(horizontals)
    verticals = np.array(verticals)
    diagonals = np.array(diagonals)

# else only get horizontals and verticals edges and set diagonals to False
else:
    n = ceil(len(edges)/2)
    horizontals = edges[0:n-1]
    verticals = edges[n-1:(2*n-1)]
    horizontals = np.array(horizontals)
    verticals = np.array(verticals)
    diagonals = False


def find_path(verticals, horizontals, t = False, diagonals = False):
    '''
    Function to find the optimal score through a given grid. The edges are read in as verticals and horizontals.
    Optional also the diagonal edges of the grid can be considered. The best score will be printed and optional
    also the best path through the grid.

    Args:
        verticals (np.array): the vertical edges of the grid
        horizontals (np.array): the horizontal edges of the grid
        t (bool): if True function prints optimal path,
            default = False
        diagonals (bool or np.array): False if no diagonal edges should be used, else np.array with the diagonal edges of the grid,
            default = False

    Returns:
        None
            prints best score and optional path through grid
    '''
    # initialize the matrix
    mat_row, mat_col = verticals.shape[0], horizontals.shape[1]
    matrix = np.zeros((mat_row, mat_col))
    matrix[0][1:] = np.cumsum(verticals[0])
    matrix[1:, 0] = np.cumsum(horizontals[:, 0])

    # if we want path, store backtracking
    if t:
        # initialize backtracking with first rows = E, and first col = S
        backtracking = np.empty(shape=(matrix.shape), dtype=object)
        backtracking[0][0] = "-"
        backtracking[0][1:] = "E"
        backtracking[1:, 0] = "S"

    # go through grid and calculate the best scores
    # first go over the rows
    for i in range(1, mat_row):
        # then go over cols
        for j in range(1, mat_col):
            scores = {}
            # save score of east and west
            east = matrix[i, j - 1]
            east_edge = verticals[i][j - 1]
            scores["E"] = east + east_edge
            south = matrix[i-1, j]
            south_edge = horizontals[i-1][j]
            scores["S"] = south + south_edge
            # optional also get score of diagonals
            if not isinstance(diagonals, bool):
                dia = matrix[i-1, j-1]
                dia_edge = diagonals[i-1][j-1]
                scores["D"] = dia + dia_edge

            # get max score
            matrix[i,j] = max(scores.values())

            # if we want path through grid, also store direction
            if t:
                backtrack = [key for key, value in scores.items() if value == max(scores.values())]
                if len(backtrack) == 1:
                    backtracking[i][j] = backtrack[0]
                else:
                    # if we have max scores, we go south
                    backtracking[i][j] = "S"

    # after going over the grid, the score is saved in the right, lower corner
    end_score = matrix[-1][-1]
    print(int(end_score) if float(end_score).is_integer() else round(end_score, 2))

    # if t, we backtrack the path
    if t:
        i, j = backtracking.shape
        # start in lower right corner
        i, j = i-1, j-1
        path = ""
        while True:
            # add corresponding stored direction of backtracking matrix to the path
            if backtracking[i][j] == "E":
                path = "E" + path
                j -= 1
            elif backtracking[i][j] == "S":
                path = "S" + path
                i -= 1
            elif backtracking[i][j] == "D":
                path = "D" + path
                i -= 1
                j -= 1

            # stop backtracking, when we land in upper left corner
            elif backtracking[i][j] == "-":
                break
        print(path)
    return


# execute the function to find optimal path
find_path(verticals, horizontals, t = args.t, diagonals=diagonals)