# Author: Sören Yannick Seitz (01508252)

import argparse
import numpy as np

def read_file(filename):
    """
    Read the input file and store the weight data in a list of lists.

    Args:
    filename (str): The name of the input file.

    Returns:
    list: A list of lists containing the weight data.
    """
    with open(filename, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        data.append(list(map(float, line.split())))

    return data

def process_data(data, diagonal):
    """
    Split the data into horizontal, vertical, and optional diagonal edge weights.

    Args:
        data (list): The list containing the weight data.
        diagonal (bool): If True, process diagonal edge weights as well.

    Returns:
        tuple: A tuple containing numpy arrays for horizontal, vertical, and optional diagonal edge weights.
    """
    x = len(data[0])
    n = len(data)
    
    # Calculate the value of m (number of horizontal edges)
    m = 0
    for row in data:
        if len(row) == x:
            m += 1
        else:
            break

    # Calculate the value of n (number of vertical edges), if diagonal seems to be present
    if x + m < n:
        n = x + m
    """
    print("x = " + str(x))
    print("n = " + str(n))
    print("m = " + str(m))
    """
    horizontal = np.array(data[:m])
    vertical = np.array(data[m:n])

    if diagonal:
        diagonal = np.array(data[n:])
    else: # ignore diagonal if flag is not set (default)
        diagonal = None

    return horizontal, vertical, diagonal

def find_path(horizontal, vertical, diagonal):
    """
    Solve the Manhattan Tourist Problem using dynamic programming.

    Args:
        horizontal (numpy.ndarray): The horizontal edge weights.
        vertical (numpy.ndarray): The vertical edge weights.
        diagonal (numpy.ndarray): The diagonal edge weights (optional).

    Returns:
        tuple: A tuple containing the weight of the longest path and the backtracking matrix for path tracing.
    """
    n = len(horizontal) + 1
    dp = np.zeros((n, n))
    backtracking = np.empty((n, n), dtype=str)

    for i in range(1, n):
        dp[i, 0] = dp[i - 1, 0] + vertical[i - 1, 0]
        backtracking[i, 0] = "S"

    for j in range(1, n):
        dp[0, j] = dp[0, j - 1] + horizontal[0, j - 1]
        backtracking[0, j] = "E"

    for i in range(1, n):
        for j in range(1, n):
            east = dp[i, j - 1] + horizontal[i - 1, j - 1]
            south = dp[i - 1, j] + vertical[i - 1, j - 1]

            if diagonal and i > 1 and j > 1:
                diag = dp[i - 1, j - 1] + diagonal[i - 2, j - 2]
                max_value, direction = max((east, "E"), (south, "S"), (diag, "D"))
            else:
                max_value, direction = max((east, "E"), (south, "S"))

            dp[i, j] = max_value
            backtracking[i, j] = direction

    best_path_weight = dp[i, j]
    if best_path_weight.is_integer():
        best_path_weight = int(best_path_weight)

    return best_path_weight, backtracking


def trace_path(backtracking):
    """
    Trace the longest path using the backtracking matrix.

    Args:
        backtracking (numpy.ndarray): The backtracking matrix containing directions.

    Returns:
        str: The longest path as a string of directions (E, S, D).
    """
    n = backtracking.shape[0]
    path = ""
    i, j = n - 1, n - 1
    while i != 0 or j != 0:
        direction = backtracking[i, j]
        path = direction + path

        if direction == "E":
            j -= 1
        elif direction == "S":
            i -= 1
        else:
            i -= 1
            j -= 1

    return path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="input file")
    parser.add_argument("-t", "--trace", help="output the longest path", action="store_true")
    parser.add_argument("-d", "--diagonal", help="allow diagonal connections", action="store_true")
    args = parser.parse_args()

    data = read_file(args.filename)
    #print(data)
    horizontal, vertical, diagonal = process_data(data, args.diagonal)
    #print(horizontal)
    #print(vertical)
    #print(diagonal)

    weight, backtracking = find_path(horizontal, vertical, diagonal)

    # print the weight of the longest path
    print(weight)
    print(backtracking)
    
    # if trace flag is set, print the best path
    if args.trace:
        path = trace_path(backtracking)
        print(path)

if __name__ == "__main__":
    main()
