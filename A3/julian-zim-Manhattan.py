import sys

if __name__ == '__main__':

    # command line arguments
    filename = ''
    t = False
    d = False
    actual_d = False

    if len(sys.argv) < 2:
        print('Usage: \"' + sys.argv[0] + ' <filename> [-d] [-t]\"')
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

    width = 0
    height = 0

    line = file.readline()
    while line:  # seek to first verticals line and determine width
        if line[0] != '#':
            data = line.split()
            if data:
                width = len(data)
                height += 1
                break
        line = file.readline()

    while line:  # read in verticals lines and determine height
        if line[0] != '#':
            data = line.split()
            if data:
                if len(data) > width or len(data) < width - 1:
                    raise Exception('Input matrix for vertical edges has wrong format (not all rows are the same length).')
                if len(data) == width - 1:
                    break
                height += 1
                verticals.append(list())
                for value in data:
                    temp = value.split('.')
                    if len(temp) > 1 and len(temp[1]) > 2:
                        raise Exception('Only two decimals per data point are allowed.')
                    verticals[-1].append(float(value))
        line = file.readline()

    counter = 0
    while counter < height:  # read in exactly height many horizontals lines
        if not line:
            raise Exception('Horizontal and vertical input matrix dimensions don\'t match.')
        if line[0] != '#':
            data = line.split()
            if data:
                if len(data) != width - 1:
                    raise Exception('Horizontal and vertical input matrix dimensions don\'t match.')
                horizontals.append(list())
                for value in data:
                    temp = value.split('.')
                    if len(temp) > 1 and len(temp[1]) > 2:
                        raise Exception('Only two decimals per data point are allowed.')
                    horizontals[-1].append(float(value))
                counter += 1
        line = file.readline()

    if d:
        counter = 0  # read in exactly height - 1 many diagonals lines
        while line and counter < height - 1:
            if line[0] != '#':
                data = line.split()
                if data:
                    if len(data) != width - 1:
                        raise Exception('Diagonal input matrix dimension doesn\'t match the horizontal and vertical ones.')
                    diagonals.append(list())
                    for value in data:
                        temp = value.split('.')
                        if len(temp) > 1 and len(temp[1]) > 2:
                            raise Exception('Only two decimals per data point are allowed.')
                        diagonals[-1].append(float(value))
                    counter += 1
            line = file.readline()
        actual_d = counter > 0
        if not actual_d:
            print('Warning: Trying to process diagonal edge information while file doesn\'t contain any.')
        elif counter != height - 1:
            raise Exception('Diagonal input matrix dimension doesn\'t match the horizontal and vertical ones.')

    garbage = False  # check for unnessecary content
    while line:
        if line[0] != '#' and line.split():
            garbage = True
            break
        line = file.readline()
    if garbage:
        print('Warning: More lines following after matrices already fully specified. '
              + ('Maybe try the -d flag?' if not d else ''))

    file.close()

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
            if d and actual_d:
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

    # output
    result = -1
    try:
        result = score_matrix[-1][-1]
    except IndexError:
        pass
    print("{:.2f}".format(result) if result != int(result) else str(int(result)))

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
