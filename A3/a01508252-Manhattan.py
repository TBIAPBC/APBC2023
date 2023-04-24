# Author: Sören Yannick Seitz (01508252)

import argparse
import numpy as np
import os

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
    # Initialise the dimensions of the grid
    #print(horizontal)
    #print(vertical)
    n = len(horizontal) + 1
    #print(n)
    m = len(vertical[0]) + 1
    #print(m)
    # Create the dynamic programming table to store path weights
    dp = np.zeros((n, m))
    # Create the backtracking table to store the directions of the longest path
    backtracking = np.empty((n, m), dtype=str)

    # Initialise the first column of the dynamic programming table
    for i in range(1, n):
        dp[i, 0] = dp[i - 1, 0] + horizontal[i - 1, 0]
        backtracking[i, 0] = "S"

    # Initialise the first row of the dynamic programming table
    for j in range(1, m):
        dp[0, j] = dp[0, j - 1] + vertical[0, j - 1]
        backtracking[0, j] = "E"

    # Fill in the dynamic programming table and the backtracking table
    for i in range(1, n):
        for j in range(1, m):
            east = dp[i, j - 1] + vertical[i, j - 1]
            south = dp[i - 1, j] + horizontal[i - 1, j]
            # If the diagonal option is enabled, consider diagonal moves as well
            if diagonal is not None:
                diag = dp[i - 1, j - 1] + diagonal[i - 1, j - 1]
                max_value, direction = max((east, "E"), (south, "S"), (diag, "D"))
            else:
                max_value, direction = max((east, "E"), (south, "S"))

            dp[i, j] = max_value       
            #dp[i, j] = east
            backtracking[i, j] = direction 


    # Get the weight of the longest path
    best_path_weight = dp[-1, -1]

    # Convert the weight to an integer if it is a whole number
    if best_path_weight.is_integer():
        best_path_weight = int(best_path_weight)
    else: # otherwise, round it to two decimal places
        best_path_weight = f"{best_path_weight:.2f}" if isinstance(best_path_weight, float) else str(best_path_weight)

    return best_path_weight, backtracking, dp


def trace_path(backtracking):
    """
    Trace the longest path using the backtracking matrix.

    Args:
        backtracking (numpy.ndarray): The backtracking matrix containing directions.

    Returns:
        str: The longest path as a string of directions (E, S, D).
    """
    # Start at the bottom right corner of the backtracking matrix and trace the path back to the top left corner
    # n = number of rows, m = number of columns
    n, m = backtracking.shape
    path = ""
    i, j = n - 1, m - 1
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
    # Add a flag to export the output to a file, to check for correctness with the test cases provided
    parser.add_argument("-p", help="export output to a file", action="store_true")
    args = parser.parse_args()

    data = read_file(args.filename)
    horizontal, vertical, diagonal = process_data(data, args.diagonal)

    weight, backtracking, dp = find_path(horizontal, vertical, diagonal)

    # Format the output
    output = str(weight)
    if args.trace:
        path = trace_path(backtracking)
        output += "\n" + str(path)
    output += "\n"
    # Print the output to the console
    print(output)

    # If the '-p' flag is set, export the output to a file
    if args.p:
        # Create the output file name by replacing the '.in' extension with '.out'
        input_basename = os.path.basename(args.filename)
        output_filename = "a01508252-" + input_basename.replace(".in", ".out")

        # Write the output to the file
        with open(output_filename, "w") as output_file:
            output_file.write(output)

if __name__ == "__main__":
    main()
