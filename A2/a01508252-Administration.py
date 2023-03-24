import sys

def read_input(file_name):
    with open(file_name, 'r') as f:
        n, cost_limit = map(int, f.readline().split())
        cities = f.readline().strip().split()
        matrix = []
        for i, line in enumerate(f.readlines(), start=3):
            row = [int(x) if x != '-' else 0 for x in line.split()]
            if len(row) != n:
                print(f"Error: row {i} has {len(row) - 1} elements, expected {n}")
                sys.exit(1)
            matrix.append(row)
    return n, cost_limit, cities, matrix

def convert_matrix_to_graph(matrix, nodes):
    graph = {}
    
    for i, node in enumerate(nodes):
        connections = {}
        for j, weight in enumerate(matrix[i]):
            if j > i:
                connections[nodes[j]] = weight
        graph[node] = connections

    return graph

def generate_city_pairs(cities):
    pairs = []
    n = len(cities)
    for i in range(n):
        for j in range(i + 1, n):
            pairs.append((cities[i], cities[j]))
    return pairs

def calculate_costs(valid_combinations, graph):
    costs = {}
    for combination in valid_combinations:
        total_cost = 0
        for pair in combination:
            total_cost += graph[pair[0]][pair[1]]
        costs[tuple(combination)] = total_cost
    return costs


def branch_and_bound(current_combination, remaining_pairs, graph, cost_limit, current_cost, no_cities):
    if len(current_combination) == no_cities // 2:
        # If we have reached the end of the recursion, return the current combination
        return [current_combination]

    valid_combinations = []

    for i, pair in enumerate(remaining_pairs):
        new_cost = current_cost + graph[pair[0]][pair[1]]

        # If the new cost is greater than the cost limit, skip this pair
        if new_cost > cost_limit:
            continue

        new_remaining_pairs = remaining_pairs[i + 1:]

        # Remove all pairs that contain any of the cities in the current pair
        for city in pair:
            new_remaining_pairs = [p for p in new_remaining_pairs if city not in p]

        new_combination = current_combination + [pair]

        # Recursively call the function with the updated combination and remaining pairs
        valid_combinations.extend(branch_and_bound(new_combination, new_remaining_pairs, graph, cost_limit, new_cost, no_cities))

    # Return all valid combinations found during the recursion
    return valid_combinations


def main():
    if len(sys.argv) < 2:
        print("Please provide a filename as a parameter.")
        sys.exit(1)

    input_file = sys.argv[1]
    calculate_optimal_costs = '-o' in sys.argv

    try:
        with open(input_file):
            pass
    except FileNotFoundError:
        print(f"The file {input_file} was not found.")
        sys.exit(1)

    #Read in data
    n, cost_limit, cities, matrix = read_input(input_file)

    #Convert matrix to graph
    graph = convert_matrix_to_graph(matrix, cities)

    #Generate city pairs
    city_pairs = generate_city_pairs(cities)

    # Find valid combinations using branch and bound
    valid_combinations_result = branch_and_bound([], city_pairs, graph, cost_limit, 0, n)

    # Calculate costs for each valid combination
    combination_costs = calculate_costs(valid_combinations_result, graph)

    # Print optimal cost if argument "-o" is provided
    if calculate_optimal_costs:
        optimal_combination = min(combination_costs, key=combination_costs.get)
        optimal_cost = combination_costs[optimal_combination]
        print(optimal_cost)
    else:  
        # Print all valid combinations
        for combination, cost in combination_costs.items():
            formatted_combination = " ".join([f"{pair[0]}{pair[1]}" for pair in combination])
            print(f"{formatted_combination}")

if __name__ == "__main__":
    main()