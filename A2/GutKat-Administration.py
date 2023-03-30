import argparse
import numpy as np

#get the arguments as input
parser = argparse.ArgumentParser(description='A2 - Optimizing the administration of Atirasu')
parser.add_argument('input', type=str, help='the input file')
parser.add_argument('-o', action='store_true', help='find the best score')
args = parser.parse_args()


def optimize(input_nodes, matrix, upper_bound) -> list:
    '''
    function to find pairs of input_nodes with a specified upper_bound

    Args:
        input_nodes (list): list of capital-names = nodes
        matrix (np.array): symmetric cost matrix
        upper_bound (int): cost limit

    return:
        results (list): list of possible pairings, which do not exceed cost limit
    '''

    #create dictionary of input, to keep track where which capital name is in the matrix
    matrix_dict = dict(map(lambda i: (input_nodes[i], i), range(len(input_nodes))))
    #initiliaze empty result list
    results = []


    def inner_function(score, current_node, free_nodes, pairs = list(), i = 0):
        '''
        recursive function to find pairings

        Args:
            score (int): score of current pairing
            current_node (str): node, which should be merged
            free_nodes (list): remaining nodes, which are not merged yet
            pairs (list): already merged nodes
            i (int): number of next node

        return:
            None: if pairing is not possible or exceeds cost limit
            merge_pairs (list), merge_score (int): pairing of nodes and score of this pairing (returned if possible pairing was found)
        '''

        #check if current node is still in free nodes, if so remove node from free nodes
        if current_node in free_nodes:
            free_nodes.remove(current_node)

        #check if there is a next free node left in free nodes, if not stop search
        try:
            next_node = free_nodes[i]  # i??
        except:
            return

        # merge next node and current node
        merge_pairs = pairs + [current_node + next_node]
        dic_A = matrix_dict[current_node]
        dic_B = matrix_dict[next_node]
        #find score in matrix
        merge_score = score + int(matrix[dic_A][dic_B])

        #if new merged score is lower than upper bound, continue to merge nodes
        if merge_score <= upper_bound:
            #create new free nodes, where merged nodes are not included
            merge_free_nodes = [x for x in free_nodes if x != next_node]

            #if there are no free nodes left, search is finished and we return pairing and score
            if not merge_free_nodes:
                return merge_pairs, merge_score

            #if there are free nodes left, we define new node as current node and continue search with this node
            merge_current_node = merge_free_nodes[0]
            #continue current search, with new score, new current node, new free nodes, and new pairs
            result = inner_function(merge_score, merge_current_node, merge_free_nodes, merge_pairs, i=0)

            #if result was found, add to results
            if result:
                results.append(result[0])

        # merge current node NOT with next node,
        # increase i by one, so the current node is merged with the next-but-one node
        inner_function(score, current_node, free_nodes, pairs, i+1)
        return

    #start search
    inner_function(0, input_nodes[0], input_nodes)
    return results


def optimize_best(input_nodes, matrix, upper_bound) -> tuple:
    '''
    function to find pairs of input_nodes with an specified upper_bound

    Args:
        input_nodes (list): list of capital-names
        matrix (np.array): symmetric cost matrix
        upper_bound (int): cost limit

    return:
        results (tuple): tuple with best score (int) and best pairing of input (list)
    '''

    #create dictionary of input, to keep track where which capital name is in the matrix
    matrix_dict = dict(map(lambda i: (input_nodes[i], i), range(len(input_nodes))))

    def inner_function(best_score, best_pairs, score, current_node, free_nodes, pairs = list(), i = 0):
        '''
        recursive function to find best score

        Args:
            best_score (int): best found score yet
            best_pairs (list): best found pairing corresponding to best score yet
            score (int): score of current pairing
            current_node (str): node, which should be merged
            free_nodes (list): remaining nodes, which are not merged yet
            pairs (list): already merged nodes
            i (int): number of next node

        return:
            None: if pairing is not possible or exceeds cost limit
            merge_pairs (list), merge_score (int): pairing of nodes and score of this pairing (returned if possible pairing was found)
        '''
        #check if current node is still in free nodes, if so remove node from free nodes
        if current_node in free_nodes:
            free_nodes.remove(current_node)

        # check if there is a next free node left in free nodes, if not stop search
        try:
            next_node = free_nodes[i]
        except:
            return

        # merge next node and current node
        merge_pairs = pairs + [current_node + next_node]
        dic_A = matrix_dict[current_node]
        dic_B = matrix_dict[next_node]
        # find score in matrix
        merge_score = score + int(matrix[dic_A][dic_B])

        # if new merged score is lower than upper bound, continue to merge nodes
        if merge_score <= upper_bound:
            # create new free nodes, where merged nodes are not included
            merge_free_nodes = [x for x in free_nodes if x != next_node]

            # if there are no free nodes left, we found a possible pairing, now we check if it is better or worse than already found best score
            if not merge_free_nodes:
                #if best score is still 0, we set best score to merge score and return it
                if best_score == 0:
                    best_score = merge_score
                    best_pairs = merge_pairs
                    return best_score, best_pairs
                #if new score is better than current best score, we set best score to merge score and return it
                elif merge_score < best_score:
                    best_score = merge_score
                    best_pairs = merge_pairs
                    return best_score, best_pairs
                #if merge score was worse than best score we return None
                else:
                    return
            # if there are free nodes left, we define new node as current node and continue search
            merge_current_node = merge_free_nodes[0]
            # continue search with new score, new current node, new free nodes, and new pairs
            result = inner_function(best_score, best_pairs, merge_score, merge_current_node, merge_free_nodes, merge_pairs, i=0)

            # if results was found, we set best score to this result
            if result:
                best_score, best_pairs = result

        # merge current node NOT with next node,
        # increase i by one, so the current node is merged with the next-but-one node
        result = inner_function(best_score, best_pairs, score, current_node, free_nodes, pairs, i+1)

        # if results was found, we set best score to this result
        if result:
            best_score, best_pairs = result

        #return the best found score and corresponding pairing
        return best_score, best_pairs

    #start search
    best_score, best_pairs = inner_function(0, [], 0, input_nodes[0], input_nodes)
    return best_score, best_pairs


if __name__ == "__main__":
    #read in content
    with open(args.input, "r") as f:
        content = f.read().split("\n")

    #split elements of content, which are seperated by a space
    content = [x.split(" ") for x in content if x]
    #remove elements of each list in content, which are None (e.g. "")
    content = [[a for a in x if a] for x in content]
    #set upper bound
    upper_bound = int(content[0][1])
    #set names of capital
    capital_names = content[1]
    #set matrix
    matrix = np.array(content[2:])

    if args.o:
        results = optimize_best(capital_names, matrix, upper_bound)
        print(results[0])
    else:
        results = optimize(capital_names, matrix, upper_bound)
        #sort results
        for result in results:
            result.sort()
        results.sort()
        for result in results:
            print(" ".join(result))
