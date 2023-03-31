def parse_file(file):
    all_matrix = []
    line_length = 0
    new_matrix = []
    for line in file:
        if line[0] == '#' or line == '\n':
            continue
        row = [float(i) for i in line.strip().split()]
        c_line_length = len(row)
        if line_length != c_line_length:
            if len(new_matrix):
                all_matrix.append(new_matrix)
            line_length = c_line_length
            new_matrix = [row]
        else:
            new_matrix.append(row)

    if len(new_matrix):
        all_matrix.append(new_matrix)
    return all_matrix


def fill_matrix_easy(m, n_s, w_e):
    for idx_r, row in enumerate(m):
        for idx_c, col in enumerate(row):
            pot_solutions = []
            try:
                if idx_c > 0:
                    pot_solutions.append(m[idx_r][idx_c-1] + w_e[idx_r][idx_c-1])
                if idx_r > 0:
                    pot_solutions.append(m[idx_r-1][idx_c] + n_s[idx_r-1][idx_c])
                if len(pot_solutions):
                    m[idx_r][idx_c] = max(pot_solutions)
            except Exception as e:
                print(f'ERROR')
    return m


def backtrace(m, n_s, w_e):
    value_path = []
    path = ''
    idx_r = len(m) - 1
    idx_c = len(m[0]) - 1
    x = 0
    while idx_r or idx_c:
        x += 1
        # CASE: reached no border
        if idx_r and idx_c:
            pot_steps = []
            # Here I create the potential steps
            row_step = m[idx_r][idx_c] - m[idx_r - 1][idx_c]
            col_step = m[idx_r][idx_c] - m[idx_r][idx_c - 1]
            # Here I am checking which steps are possible according to the step-matrices
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
        step = max(pot_steps)
        # If there would be multiple solution I would need to makle some error handling here like:
        # print(f'From [{idx_r}|{idx_c}] {pot_steps = }')
        #if 60 < x and x < 70:
         #   print(f'From [{idx_r}|{idx_c}] {pot_steps = }')

        #if step == pot_steps[0] and step == pot_steps[1]:
         #   print('A')
          #  idx_r = idx_r - 1
           # path = path + 'S'
       # else:
        value_path.append(step)
        i = pot_steps.index(step)
        if i:
            idx_c = idx_c - 1
            path = path + 'E'
        else:
            idx_r = idx_r - 1
            path = path + 'S'
    # print(value_path)
    return path[::-1]

