import argparse


def create_new_key(p, t1, t2):
    new_key_elements = []
    if p:
        new_key_elements = p.split(',')
    new_key_elements.append(str(t1 + t2))
    new_key = ','.join(sorted(new_key_elements))
    return new_key


def get_all_pairs_recursion(pairs, adj_list, max_cost):
    new_pairs = {}
    for pair_keys, rem_data in pairs.items():
        rem_towns = rem_data[0]
        rem_cost = rem_data[1]

        unique_new_tuples = set({})

        for idx1, town_1 in enumerate(rem_towns):
            for idx2, town_2 in enumerate(rem_towns):
                # create the new town-tuple to see if it is a dupplicate
                new_town_tuple = str(sorted([town_1, town_2]))
                if idx1 != idx2 and new_town_tuple not in unique_new_tuples:
                    # remove the selected towns from the remaining towns of this solution and calculate aggregated cost
                    new_rem_towns = rem_towns.copy()
                    new_rem_towns.remove(town_1)
                    new_rem_towns.remove(town_2)
                    new_cost = rem_cost + adj_list[town_1][town_2]
                    # check if result is more expensive than price-cap & if town-set is unique
                    if new_cost <= max_cost:
                        unique_new_tuples.add(new_town_tuple)
                        new_key = create_new_key(pair_keys, town_1, town_2)
                        # if all these requests are fulfilled we add the solution to our potential solutions
                        new_pairs[f'{new_key}'] = (new_rem_towns, new_cost)

    # If the remaining set of towns is empty, this means we cannot go any further and the algorithm finishes
    if not list(pairs.values())[0][0]:
        n_pairs = sorted(set(pairs.keys()))
        minimum = min(pairs.items(), key=lambda item: item[1])[1][1]
        result_sets = []
        for pair_keys in n_pairs:
            result_sets.append(tuple(pair_keys.split(',')))
        return result_sets, minimum
    # If there is no potential solution at this point we also cannot continue
    if not new_pairs.keys():
        return f'No solution found for the current maximal cost ({max_cost})!'
    # If no ending statement is true the recursion goes on
    return get_all_pairs_recursion(new_pairs, adj_list, max_cost)


def get_administration(a_list, m_cost, optimal):
    all_towns = list(a_list.keys())
    all_towns = (all_towns, 0)
    tmp = {'': all_towns}
    pairs, min_cost = get_all_pairs_recursion(tmp, a_list, m_cost)
    if optimal:
        print(min_cost)
    else:
        for res in pairs:
            print(' '.join(res))
    return pairs, min_cost


# Input is read from command line
parser = argparse.ArgumentParser()
parser.add_argument("input", help="file name")
parser.add_argument("-o", "--optimal", action="store_true", help="Returns the minimal cost, uses max-cost as boundary")
args = parser.parse_args()
file_name = args.input
optimal_arg = args.optimal

# Here I read in the file and save the adjacencies as an adjacency list ('ad_list')
ad_list = {}
with open(file_name, 'r') as file:
    temp = {}
    max_money = int(file.readline().strip().split()[1])
    for j, node in enumerate(file.readline().strip().split()):
        temp[j] = node
    for i, row in enumerate(file):
        values = row.strip().replace('-', '0').split()
        to = {}
        for x, v in enumerate(values):
            if temp[i] != temp[x]:
                to[temp[x]] = int(v)
        ad_list[temp[i]] = to

# This function does the computing
result, minimum_cost = get_administration(ad_list, max_money, optimal_arg)
