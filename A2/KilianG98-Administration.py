#!/usr/bin/env python3

import sys
import argparse
import pandas as pd


# Optimizing the administration of Atirasu - Exercise A2

parser = argparse.ArgumentParser(description='Administration optimization')
parser.add_argument('input', help='Name of the input file')
parser.add_argument('-o', action='store_true', help='Return optimal solution')

args = parser.parse_args()

#function to calculate distance between two cities
def Score(path, df):
    score = 0
    for pair in path:
        score += df.loc[pair[0],pair[1]]
    return score

#function to check if a given path is complete
def IsComplete(path, numOfCities):
    if len(path) == numOfCities/2:
        return True
    return False

#function to check if a given city is contained in the current path
def CityInPath(city, path):
    for pair in path:
        for c in pair:
            if city == c:
                return True
    return False

# Recursive Branch and Bound. 
# Receives the cost-matrix as df, the number of cities,
# a list of paths that initially is empty and contains the solutions in the end and a set of explored paths.
def BAB(df, numOfCities, listOfPaths, exploredPaths):

    #look at the latest path
    path = listOfPaths[-1]
    global upper
    #evaluate the score of the current path, discard it if its too costly.
    if Score(path, df) > upper:
        listOfPaths.remove(path)
        if not listOfPaths:
            listOfPaths.append([])
        return 
    #return if the path is complete
    if IsComplete(path, numOfCities):
        if args.o:
            upper = Score(path, df)
        return 
    #remove the path, later add the updated path again
    listOfPaths.remove(path)
    #add new path to the list and call BAB again
    for city in df.columns:
        if not CityInPath(city, path):
            for city2 in df.columns:
                if city2 != city and not CityInPath(city2, path):
                    newP = path.copy()
                    newP.append([city,  city2])
                    newPSet = frozenset(map(frozenset, newP))
                    #add the path only if its not already explored
                    if newPSet not in exploredPaths:
                        exploredPaths.append(newPSet)
                        listOfPaths.append(newP.copy())
                        BAB(df,numOfCities, listOfPaths, exploredPaths)

    return listOfPaths

#main function
if __name__=="__main__":
    #read the cost-matrix
    with open(args.input) as f:
        vars = f.readline().strip().split()
        header = f.readline().strip().split()
        lines = [line.strip().split() for line in f.readlines()]

        matrix = []
        for line in lines:
            row = []
            for num in line:
                try:
                    row.append(int(num))
                except ValueError:
                    row.append(0)
            matrix.append(row)
        
    if int(vars[0]) % 2 == 1:
        print("Unable to make pairs of two with odd amount of cities")
        sys.exit()

    #define global cost-limit
    global upper 
    upper = int(vars[1])
    #convert matrix into pandas dataframe
    df = pd.DataFrame(matrix, columns=header, index=header)

    #get the solution
    paths = BAB(df, int(vars[0]), [[]], [])

    #print solution
    try:
        paths.remove([])
    except:
        pass
    if args.o:
        print(upper)
    else:
        for path in paths:
            for p in path:
                print(*p, sep="", end=" ")
            print("")