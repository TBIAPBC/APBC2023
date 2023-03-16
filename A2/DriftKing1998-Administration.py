import numpy as np
import itertools


def get_pair(pairs, a_list):
    new_pairs = {}
    for p, rem_towns in pairs.items():
        set_different = set({})

        for i, town in enumerate(rem_towns):
            for j, partner in enumerate(rem_towns):
                if i != j:
                    remaining = rem_towns.copy()
                    remaining.remove(town)
                    remaining.remove(partner)
                    key = str(sorted([town, partner]))
                    if key not in set_different:
                        set_different.add(key)
                        #new_cost = rem_towns[1] + a_list[town][partner]
                        new_pairs[f'{p}{town}{partner},'] = remaining

    if not list(pairs.values())[0]:
        pairs = sorted(set(pairs.keys()))
        result = []
        for p in pairs:
            result.append(tuple(p[:-1].split(',')))
        return result

    return get_pair(new_pairs, a_list)


def get_possibilities(a_list):
    all_towns = list(a_list.keys())
    #all_towns = [all_towns, 0]
    tmp = {'': all_towns}
    pairs = get_pair(tmp, a_list)
    return pairs


ad_list = {}

with open('Administration-test1.in', 'r') as file:
    tmp = {}
    max_money = file.readline().strip().split()[1]
    for j, node in enumerate(file.readline().strip().split()):
        tmp[j] = node
    for i, row in enumerate(file):
        values = row.strip().replace('-','0').split()
        to = {}
        for x, v in enumerate(values):
            if tmp[i] != tmp[x]:
                to[tmp[x]] = int(v)
        ad_list[tmp[i]] = to


print(get_possibilities(ad_list))
exit()

for k, v in ad_list.items():
    print(k, v)