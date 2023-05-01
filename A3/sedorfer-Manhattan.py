import numpy as np
import argparse as ap


def read_weights(path, diag):
    """
    Parses input file into weight matrices
    :param path: path to file
    :param diag: whether a diagonal matrix needs to be parsed
    :return: matrices with weights in the different directions
    """
    with open(path, "r") as f:
        text = f.readlines()
        weights = list()
        weights_down = list()
        weights_right = list()
        weights_diag = list()
        for line in text:
            if line.isspace():      # ignores all empty lines
                continue
            if "#" in line:     # ignores comments
                ix = line.find("#")
                if ix == 0:
                    continue
                else:
                    line = line[:ix]
            weights.append(line.split())
    length = len(weights[0])
    for w in weights:       # parses the different directions
        if len(w) == length:
            weights_down.append(w)
        else:
            weights_right.append(w)
    if diag:
        n_diag = len(weights_down) + 1
        weights_diag = weights_right[n_diag:]
        weights_right = weights_right[:n_diag]
    matrix_down = np.array(weights_down, dtype=float)
    matrix_right = np.array(weights_right, dtype=float)
    matrix_diag = np.array(weights_diag, dtype=float)
    return matrix_down, matrix_right, matrix_diag


def build_solutions(solutions, backtracing, matrix_down, matrix_right, matrix_diag, diag):
    """
    populates the matrix for the subsolutions and memorizes directions
    :param solutions: empty matrix to memorize subsolutions
    :param backtracing: empty matrix to memprize directions
    :param matrix_down: weight matrix
    :param matrix_right: weight matrix
    :param matrix_diag: weight matrix
    :param diag: whether diagonal options need to be considered
    """
    initialize_matrix(solutions, backtracing, matrix_down, matrix_right)
    for i in range(1, solutions.shape[0]):      # iteratively calculates subsolutions
        for j in range(1, solutions.shape[1]):
            down = solutions[i-1, j] + matrix_down[i-1, j]
            right = solutions[i, j-1] + matrix_right[i, j-1]
            diagonal = 0
            if diag:
                diagonal = solutions[i-1, j-1] + matrix_diag[i-1, j-1]
            solutions[i, j] = max(down, right, diagonal)
            if solutions[i, j] == down:
                path = backtracing[i-1][j] + "S"
            elif solutions[i, j] == right:
                path = backtracing[i][j-1] + "E"
            elif solutions[i, j] == diagonal:
                path = backtracing[i-1][j-1] + "D"
            backtracing[i][j] = path


def initialize_matrix(solutions, backtracing, matrix_down, matrix_right):
    """
    Fills in the first row and column of the solution matrix, as there is only one viable solution
    :param solutions: matirx for subsolutions
    :param backtracing: matrix for the traceback
    :param matrix_down: weight matrix
    :param matrix_right: weight matrix
    """
    for i in range(1, solutions.shape[1]):
        solutions[0, i] = solutions[0, i-1] + matrix_right[0, i-1]
        backtracing[0][i] = backtracing[0][i-1] + "E"
    for i in range(1, solutions.shape[0]):
        solutions[i, 0] = solutions[i-1, 0] + matrix_down[i-1, 0]
        backtracing[i][0] = backtracing[i-1][0] + "S"


def manhattan_solver(matrix_down, matrix_right, matrix_diag, diag, t):
    """
    solves the Manhattan Tourist Problem with a bottom up Dynamic Programming approach
    :param matrix_down: weight matrix
    :param matrix_right: weight matrix
    :param matrix_diag: weight matrix
    :param diag: whether to consider diagonal directions
    """
    solutions = np.zeros((matrix_right.shape[0], matrix_down.shape[1]))
    backtracing = [["" for columns in range(matrix_down.shape[1])] for rows in range(matrix_right.shape[0])]
    build_solutions(solutions, backtracing, matrix_down, matrix_right, matrix_diag, diag)
    row_ix = solutions.shape[0] - 1
    column_ix = solutions.shape[1] - 1
    optimum = solutions[row_ix, column_ix]
    if int(str(optimum).split(".")[1]) == 0:    # formatting of the output
        print(int(optimum))
    else:
        print("%.2f" % optimum)
    if t:
        print(backtracing[row_ix][column_ix])


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Manhattan Tourist Problem")
    parser.add_argument("path", help="path to input file")
    parser.add_argument("-d", action="store_true", help="allows diagonal input")
    parser.add_argument("-t", action="store_true", help="list best path")
    args = parser.parse_args()
    matrix_down, matrix_right, matrix_diag = read_weights(args.path, diag=args.d)
    manhattan_solver(matrix_down, matrix_right, matrix_diag, diag=args.d, t=args.t)
