import numpy as np
import itertools


def create_new_key(p, t1, t2):
    new_key_elements = []
    if p:
        new_key_elements = p.split(',')
    new_key_elements.append(str(t1 + t2))
    new_key = ','.join(sorted(new_key_elements))
    return new_key


def get_possible_pairs(pairs, a_list, max_cost):
    new_pairs = {}
    for pair_keys, data_left in pairs.items():
        rem_towns = data_left[0]
        rem_cost = data_left[1]

        unique_new_tuples = set({})

        for i, town_1 in enumerate(rem_towns):
            for j, town_2 in enumerate(rem_towns):
                if i != j:
                    new_rem_towns = rem_towns.copy()
                    new_rem_towns.remove(town_1)
                    new_rem_towns.remove(town_2)

                    new_town_tuple = str(sorted([town_1, town_2]))
                    new_cost = rem_cost + a_list[town_1][town_2]

                    if new_cost <= max_cost and new_town_tuple not in unique_new_tuples:
                        unique_new_tuples.add(new_town_tuple)
                        new_key = create_new_key(pair_keys, town_1, town_2)
                        new_pairs[f'{new_key}'] = (new_rem_towns, new_cost)

    # If the remaining set of towns is empty, this means all solutions have been found
    if not list(pairs.values())[0][0]:
        n_pairs = sorted(set(pairs.keys()))
        minimum = (list(pairs.values())[1])
        print(minimum)
        result = []
        for pair_keys in n_pairs:
            result.append(tuple(pair_keys.split(',')))
        return result

    # If there is no potential solution at this point we also cannot continue
    if not new_pairs.keys():
        return f'No solution found for the current maximal cost {max_cost}!'

    # If no ending statement is true the recursion goes on
    # print(new_pairs)
    return get_possible_pairs(new_pairs, a_list, max_cost)


def get_possibilities(a_list, m_cost):
    all_towns = list(a_list.keys())
    all_towns = (all_towns, 0)
    tmp = {'': all_towns}
    pairs = get_possible_pairs(tmp, a_list, m_cost)
    return pairs


ad_list = {}

with open('Administration-test1.in', 'r') as file:
    temp = {}
    max_money = file.readline().strip().split()[1]
    for j, node in enumerate(file.readline().strip().split()):
        temp[j] = node
    for i, row in enumerate(file):
        values = row.strip().replace('-', '0').split()
        to = {}
        for x, v in enumerate(values):
            if temp[i] != temp[x]:
                to[temp[x]] = int(v)
        ad_list[temp[i]] = to
    
result = get_possibilities(ad_list, 9)

#print(f'The were {len(result)} solutions:\n{result}')

for res in result:
    print(' '.join(res))
