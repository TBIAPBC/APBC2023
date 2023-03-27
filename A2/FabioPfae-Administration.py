"""
- 8 provinces, 4 authorities, solution: set of 4 pairs (4 subsets of 2 old_pairsents each)
      from set of capitals   {B,E,G,I,K,L,P,S}
- cost dependent on combination of pairs (matrix)
- #provinces (even) and cost limit parameters shall be abitrary
- input: text file with matrix and parameters (cost limit refers to the sum of all 4 entries)
- output: all possible combinatoins that dont exceed cost limit (print,
          each line a solution)
          e.g (BE GI KL SP) refers to the partition {{B,E},{G,I},{K,L},{P,S}}
- avoid redundant output due to permutations. Choose lexicographically smallest.

flags:
-o -> optimize the cost (instead of enumerating), use cost limit as initial bound.
    output: score of the best solution

hints:
- branch and bound strategy for both parts (For the first partition: bound does not have to be adapted
with every new solution)


  8 10                     # number of capitals; cost limit
     B  E  G  I  K  L  P  S  # cities of capitals
  B  - 10 10  2 10 10 10 10  # symmetric cost matrix
  E 10  -  2 10 10 10  1 10
  G 10  2  - 10  2  3  3  3
  I  2 10 10  -  4 10 10  2
  K 10 10  2  4  - 10 10  3
  L 10 10  3 10 10  -  2  2
  P 10  1  3 10 10  2  - 10
  S 10 10  3  2  3  2 10  -

  """

import sys

def Input(file): #returns all important parameters
    file = open(file).readlines()   
    
    cap = int(file[0].split()[0])
    lim = int(file[0].split()[1])
    cities = file[1].strip().split()

    costs = [] # cost matrix
    for i in range(2,len(file)):
        costs.append(file[i].replace("\n","").split())
    for i in range(len(costs)):
        for j in range(len(costs[i])):
            if costs[i][j] == '-':
                costs[i][j] = lim+1
            else:
                costs[i][j] = int(costs[i][j])
    
    pairs = [] # all possible pairs faculty of number of cities-1
    sub = []
    n = len(costs)

    for i in range(n-1):
        for j in range(i+1, n):
            sub.append([cities[i], cities[j]])
        pairs.append(sub)
        sub = []
    
    return [cap, lim, cities, pairs, costs]

def PairCost(pair): #cost for one pair
    first = cities.index(pair[0]) 
    second = cities.index(pair[1])
    return costs[first][second]

def CurrentLoad(pairs): #cost for an array of pairs
    total = 0
    if pairs == []: return total
    for i in pairs:
        total+= PairCost(i)
    return total

def IsNotContained(new_pair, entry): #returns True if pair of interest (new_pair) is not in an array of pairs (entry)
    for pair in entry:
        for city in pair:
            if city in new_pair:
                return False
    return True

# generates a tree structure with first level (root children) = the first row 
# of "pairs", each having has children the second row of "pairs", and so on. 
# A Path is discarded if it exceeds the cost.
# A Child/Pair is not added if one of its letters/cities is already contained in the path.
# First for loop, iterates over all rows of "pairs" which correspond to the level of the tree
# Second for loop, iterates over my solution array, which shall contain all valid paths in the end..
# .. at the beginning my solution array is empty
# Third loop iterates over all the pairs of "pairs" rows
# 1st iteration: sol contains all elements of the first row
# 2nd iteration: each element of 1st sol is added to each element of the 2nd row creating length(row1)*length(row2) arrays
# Same goes on for the next iterations
def BranchAndBound(pairs): 
    sol = [[]]
    for row in pairs:
        temp = []
        for entry in sol:
            for new_pair in row:
                if CurrentLoad(entry) + PairCost(new_pair) <= lim and IsNotContained(new_pair, entry):
                    temp.append(entry + [new_pair])
                elif not IsNotContained(new_pair, entry):
                    temp.append(entry)
        sol = temp
    
    final = [] # unfortunately sol contained a bunch of non valid entries, either the entries are redundant
    for i in sol: #or the partition length is smaller than it should be, with this block i cropped them out.
        if len(i) == cap/2 and i not in final:
            final.append(i)
    return final

def main():
    arg = sys.argv
    global cap, lim, cities, pairs, costs
    input = Input(arg[1])
    
    cap = input[0]
    lim = input[1]
    cities = input[2]
    pairs = input[3]
    costs = input[4]

    print("cities\n", cities)
    print("\n#cities:", cap, ", limit:", lim)

    print("\ncosts")
    for i in costs:
        print(i)
    
    print("\npairs")                 
    for i in pairs:
        print(i)
    print()

    solutions = BranchAndBound(pairs)
    try:
        if arg[2] == "-o":
            min = solutions[0]
            for i in solutions:
                if CurrentLoad(i) < CurrentLoad(min):
                    min = i
            print("cheapest partition\n", min, "with cost", CurrentLoad(min))
        else:
            print("false parameter for generating optimum value, use -l")
                    

    except:
        print("\nsolutions:")
        for i in solutions:
            print(i)
        
        
    print("\nfinished.")

if __name__ == "__main__":
    main()
