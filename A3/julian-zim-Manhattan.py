import sys
import math

if __name__ == '__main__':

    # parsing
    d = False
    t = False
    filename = ''

    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' <filename> [-d] [-t]')
        sys.exit()

    for argument in sys.argv[1:]:
        if argument[0] == '-':
            if argument == '-d':
                d = True
            elif argument == '-t':
                t = True
            else:
                raise Exception('Unknown flag: ' + argument + '!')
        else:
            if filename == '':
                filename = argument
            else:
                raise Exception('Unexpected argument: ' + argument + '! A filename was already specified.')

    # file
    file = open(filename)
    verticals = list()
    horizontals = list()
    diagonals = list()

    width = -math.inf
    height = -math.inf

    # skip to first verticals line
    line = file.readline()
    while line:
        if line != '\n' and line[0] != '#':
            width = len(line.split())
            break
        line = file.readline()

    # read in verticals lines
    while line:
        if line != '\n' and line[0] != '#':
            if len(line.split()) < width:
                break
            else:
                verticals.append(list())
                for value in line.split():
                    verticals[-1].append(float(value))
        line = file.readline()

    # read in horizontals lines
    counter = 0
    while counter < width and line:
        if line != '\n' and line[0] != '#':
            horizontals.append(list())
            for value in line.split():
                horizontals[-1].append(float(value))
            counter += 1
        line = file.readline()
    height = counter

    if d:
        d_counter = 0
        while d_counter < height - 1 and line:
            if line != '\n' and line[0] != '#':
                diagonals.append(list())
                for value in line.split():
                    diagonals[-1].append(float(value))
                d_counter += 1
            line = file.readline()

    # algorithm
    score_matrix = [[0 for _ in range(width)] for _ in range(height)]
    source_matrix = [['-' for _ in range(width)] for _ in range(height)]

    for i in range(1, len(score_matrix)):
        score_matrix[i][0] = score_matrix[i - 1][0] + verticals[i - 1][0]
        source_matrix[i][0] = 'S'

    for j in range(1, len(score_matrix[0])):
        score_matrix[0][j] = score_matrix[0][j - 1] + horizontals[0][j - 1]
        source_matrix[0][j] = 'E'

    for i in range(1, len(score_matrix)):
        for j in range(1, len(score_matrix[i])):
            if i == 0 and j == 0:
                continue

            top_score = score_matrix[i - 1][j] + verticals[i - 1][j]
            left_score = score_matrix[i][j - 1] + horizontals[i][j - 1]
            diag_score = -1
            best_score = -1
            if d:
                diag_score = score_matrix[i - 1][j - 1] + diagonals[i - 1][j - 1]
                best_score = max(top_score, left_score, diag_score)
            else:
                best_score = max(top_score, left_score)
            score_matrix[i][j] = round(best_score, 2)

            if best_score == top_score:
                source_matrix[i][j] = 'S'
            elif best_score == left_score:
                source_matrix[i][j] = 'E'
            elif d and best_score == diag_score:
                source_matrix[i][j] = 'D'
            else:
                raise Exception('what')

    print("{:.2f}".format(score_matrix[-1][-1]))
    if t:
        path = list()
        index = [len(score_matrix) - 1, len(score_matrix[len(score_matrix) - 1]) - 1]
        while index[0] != 0 or index[1] != 0:
            source = source_matrix[index[0]][index[1]]
            path.insert(0, source)
            if source == 'S':
                index = [index[0] - 1, index[1]]
            if source == 'E':
                index = [index[0], index[1] - 1]
            if source == 'D':
                index = [index[0] - 1, index[1] - 1]
        print(''.join(path))
