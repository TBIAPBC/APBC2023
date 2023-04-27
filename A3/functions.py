def parse_file(file):
    all_matrix = []     # all matrices will be appended to this list
    line_length = 0
    new_matrix = []     # next matrix
    for line in file:
        # if a '#' is encountered we add the current matrix if it exists
        if line[0] == '#' or line == '\n':
            if len(new_matrix):
                all_matrix.append(new_matrix)
                new_matrix = []
        # otherwise we encode the row
        else:
            row = [float(i) for i in line.strip().split()]
            c_line_length = len(row)
            # if the length of the rows change, we add the current matrix if it exists
            if line_length != c_line_length:
                if len(new_matrix):
                    all_matrix.append(new_matrix)
                line_length = c_line_length
                new_matrix = [row]
            else:
                new_matrix.append(row)
    # at the end we add the last matrix if it exits (since sometimes there is no '#' at the end
    if len(new_matrix):
        all_matrix.append(new_matrix)

    return all_matrix


def fill_matrix_hard(m, n_s, w_e, diag):
    # looping through the array we created
    for idx_r, row in enumerate(m):
        for idx_c, col in enumerate(row):
            pot_solutions = []
            try:
                # here I create all the potential steps
                if idx_c > 0:
                    pot_solutions.append(m[idx_r][idx_c-1] + w_e[idx_r][idx_c-1])
                if idx_r > 0:
                    pot_solutions.append(m[idx_r-1][idx_c] + n_s[idx_r-1][idx_c])
                if idx_c > 0 and idx_r > 0:
                    pot_solutions.append(m[idx_r-1][idx_c-1] + diag[idx_r-1][idx_c-1])
                if len(pot_solutions):
                    # here I choose the best one considering the earlier cell
                    m[idx_r][idx_c] = max(pot_solutions)
            except Exception:
                print(f'ERROR')
    return m


def fill_matrix_easy(m, n_s, w_e):
    # looping through the array we created
    for idx_r, row in enumerate(m):
        for idx_c, col in enumerate(row):
            pot_solutions = []
            try:
                # here I create all the potential steps
                if idx_c > 0:
                    pot_solutions.append(m[idx_r][idx_c-1] + w_e[idx_r][idx_c-1])
                if idx_r > 0:
                    pot_solutions.append(m[idx_r-1][idx_c] + n_s[idx_r-1][idx_c])
                if len(pot_solutions):
                    # here I choose the best one considering the earlier cell
                    m[idx_r][idx_c] = max(pot_solutions)
            except Exception:
                print(f'ERROR')
    return m


def backtrace(m, n_s, w_e):
    path = ''
    idx_r = len(m) - 1
    idx_c = len(m[0]) - 1
    while idx_r or idx_c:
        pot_steps = []
        # CASE: reached no border
        if idx_r and idx_c:
            # Here I create the potential steps
            row_step = m[idx_r][idx_c] - m[idx_r - 1][idx_c]
            col_step = m[idx_r][idx_c] - m[idx_r][idx_c - 1]
            # Here I am checking which steps are possible according to the step-matrices
            # I always add a (-1) if the step is not possible, so that the indices are always the same
            if row_step == n_s[idx_r - 1][idx_c]:
                pot_steps.append(row_step)
            else:
                pot_steps.append(-1)
            if col_step == w_e[idx_r][idx_c - 1]:
                pot_steps.append(col_step)
            else:
                pot_steps.append(-1)
        # CASE: reached left border
        elif idx_r:
            pot_steps = [m[idx_r - 1][idx_c], -1]
        # CASE: reached upper border
        else:
            pot_steps = [-1, m[idx_r][idx_c - 1]]
        # finding the best step and adding the corresponding direction to the path-string
        multiple_steps = all(val > 0 for val in pot_steps)
        step = max(pot_steps)
        # If there would be multiple steps possible, we go 'South':
        if multiple_steps:
            idx_r = idx_r - 1
            path = path + 'S'
        else:
            i = pot_steps.index(step)
            if i:
                idx_c = idx_c - 1
                path = path + 'E'
            else:
                idx_r = idx_r - 1
                path = path + 'S'
    return path[::-1]


def backtrace_hard(m, n_s, w_e, diag):
    path = ''
    idx_r = len(m) - 1
    idx_c = len(m[0]) - 1
    while idx_r or idx_c:
        pot_steps = []
        # CASE: reached no border
        if idx_r and idx_c:
            # Here I create the potential steps
            row_step = round(m[idx_r][idx_c] - m[idx_r - 1][idx_c], 2)
            col_step = round(m[idx_r][idx_c] - m[idx_r][idx_c - 1], 2)
            diag_step = round(m[idx_r][idx_c] - m[idx_r - 1][idx_c - 1], 2)
            # Here I am checking which steps are possible according to the step-matrices
            # I always add a (-1) if the step is not possible, so that the indices are always the same
            if row_step == n_s[idx_r - 1][idx_c]:
                pot_steps.append(row_step)
            else:
                pot_steps.append(-1)
            if col_step == w_e[idx_r][idx_c - 1]:
                pot_steps.append(col_step)
            else:
                pot_steps.append(-1)
            if diag_step == diag[idx_r - 1][idx_c - 1]:
                pot_steps.append(diag_step)
            else:
                pot_steps.append(-1)
        # CASE: reached left border
        elif idx_r:
            pot_steps = [m[idx_r - 1][idx_c], -1]
        # CASE: reached upper border
        else:
            pot_steps = [-1, m[idx_r][idx_c - 1]]
        # finding the best step and adding the corresponding direction to the path-string
        multiple_steps = all(val > 0 for val in pot_steps)
        step = max(pot_steps)
        # If there would be multiple steps possible, we go 'South':
        if multiple_steps:
            print(f'MULTIPLE STEPS: {pot_steps}')
            idx_r = idx_r - 1
            path = path + 'S'
        else:
            i = pot_steps.index(step)
            if i == 0:
                idx_r = idx_r - 1
                path = path + 'S'
            elif i == 1:
                idx_c = idx_c - 1
                path = path + 'E'
            elif i == 2:
                idx_c = idx_c - 1
                idx_r = idx_r - 1
                path = path + 'D'
    return path[::-1]
