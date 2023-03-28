# python julian-zim-Administration.py Administration-test2.in [-o]

import math
import numpy
import sys


def solve_recursive(remaining_cities, previous_cost):

    # exit condition
    if len(remaining_cities) <= 2:
        city_one = remaining_cities[0]
        city_two = remaining_cities[1]

        additional_cost = int(cost_matrix[id_lookup[city_one]][id_lookup[city_two]])
        if previous_cost + additional_cost <= limit:
            return [{frozenset([city_one, city_two])}], [additional_cost]
        else:
            return [], [0]

    good_partitionings = list()
    good_costs = list()
    best_cost = limit

    # for every remaining city pair C1 C2:
    i = 0  # for i in range(0, len(remaining_cities)):
    for j in range(i + 1, len(remaining_cities)):
        city_one = remaining_cities[i]
        city_two = remaining_cities[j]

        # check if it already exceeds limit
        additional_cost = int(cost_matrix[id_lookup[city_one]][id_lookup[city_two]])
        new_cost_min = previous_cost + additional_cost
        if new_cost_min <= limit:

            # define subtree and get every solution of it
            subtree_cities = remaining_cities.copy()
            del subtree_cities[j]
            del subtree_cities[i]
            subtree_partitionings, subtree_costs = solve_recursive(subtree_cities, new_cost_min)

            # combine city pair with every subtree solution or replace if cost optimazation is enabled
            additional_partition_pair = frozenset([city_one, city_two])
            for index in range(len(subtree_partitionings)):
                subtree_partitioning = subtree_partitionings[index]
                current_cost = additional_cost + subtree_costs[index]
                subtree_partitioning.add(additional_partition_pair)

                if o:
                    if current_cost <= best_cost:
                        best_cost = current_cost
                        good_costs = [best_cost]
                        good_partitionings = [subtree_partitioning]

                else:
                    good_costs.append(current_cost)
                    good_partitionings.append(subtree_partitioning)

    return good_partitionings, good_costs


if __name__ == '__main__':

    # arguments
    if len(sys.argv) > 3:
        raise Exception('Usage: ./' + sys.argv[0] + ' -<filename> [-o]')
    args = sys.argv[1:]

    filename = args[0]
    o = False
    if args[-1] == '-o':
        o = True

    # file
    file = open(filename, 'r')
    number, limit = file.readline().split()
    number = int(number)
    limit = int(limit)
    cities = file.readline().split()

    cost_matrix = list()
    line = file.readline()
    while line:
        cost_matrix.append(line.split())
        line = file.readline()
    cost_matrix = numpy.array(cost_matrix)

    id_lookup = dict()
    for city_id in range(len(cities)):
        id_lookup[cities[city_id]] = city_id

    # solve
    partitionings, costs = solve_recursive(cities, 0)

    '''filtered_partitionings = dict()
    for n in range(len(partitionings)):
        partitioning = partitionings[n]
        cost = costs[n]

        filtered_partitionings[frozenset(partitioning)] = cost'''

    # output
    if o:
        print(costs[0])

    else:
        results_list = list()
        for partitioning in partitionings:  # filtered_partitionings:
            result_list = list()
            for pair in partitioning:
                pair_list = list()
                for city in pair:
                    pair_list.append(city)
                pair_list.sort()
                result_list.append(pair_list)
            result_list.sort()
            results_list.append(result_list)
        results_list.sort()

        results_string = str()
        for result_list in results_list:
            result_string = str()
            for pair in result_list:
                pair_string = str()
                for city in pair:
                    pair_string += city
                result_string += pair_string + ' '
            results_string += result_string + '\n'

        print(results_string)
