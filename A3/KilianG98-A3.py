#!/usr/bin/env python3

import argparse

#parse inputs
parser = argparse.ArgumentParser()
parser.add_argument('input', help = 'name of the input file')
parser.add_argument('-d', action='store_true', help='accept diagonal inputs')
parser.add_argument('-t', action='store_true', help='print optimal path')
args = parser.parse_args()

#function to read the input file
def readFile():
    #extract only the numbers from the input file and store them in a matrix
    with open (args.input) as f:
        matrix = []
        for line in f:
            if line[0]!= "#":
                row = []
                line=line.split()
                for num in line:
                    row.append(float(num))
                if row != []:
                    matrix.append(row)
    
    width=len(matrix[0])
    global vWeights
    global hWeights
    vWeights=[]
    hWeights=[]

    if args.d:
        #diagonal weights only if needed
        global dWeights
        dWeights=[]
        #read each row of the matrix until the length of the row changes, remember the number of rows (stored as height).
        #the length of the row ALWAYS changes. Vertical weights have one more element in each row when compared to horizontal weights.
        height= 0
        for row in matrix:
            if len(row)== width:
                vWeights.append(row)
                height+=1
            else:
                break
        #read the horizontal weights. The range can be calculated, because there must be one more row of the hWeights than of the vWeights.
        for i in range(height, 2*height +1):
            hWeights.append(matrix[i])
        #the rest of the matrix is diagonal weights.
        for i in range(2*height +1, len(matrix)):
            dWeights.append(matrix[i])
    else:
        #reading the matrix w/o diagonal weights is simpler, the principle is the same.
        for row in matrix:
            if len(row)==width:
                vWeights.append(row)
            else:
                hWeights.append(row)
            

def main():

    readFile()
    #intialise costMatrix with 0 in every position
    costMatrix=[]
    for i in range(len(hWeights)):
        costMatrix.append([])
        for j in range(len(vWeights[0])):
            costMatrix[i].append(0)

    #loop through every element of the cost matrix, calculate the maximum from all possible predecessors
    for i, row in enumerate(costMatrix):
        for j in range (len(row)):
            if i==0:
                if j==0:
                    pass
                else:
                    costMatrix[i][j]=round(row[j-1]+hWeights[0][j-1],2)

            elif j==0:
                costMatrix[i][j]=round(costMatrix[i-1][0] +vWeights[i-1][0],2)

            else:
                tmpUp=costMatrix[i-1][j] + vWeights[i-1][j]
                tmpLeft=costMatrix[i][j-1] + hWeights[i][j-1]

                if args.d:
                    tmpDiag=costMatrix[i-1][j-1]+dWeights[i-1][j-1]
                else:
                    tmpDiag=0
                    
                costMatrix[i][j]=round(max(tmpUp, tmpLeft,tmpDiag),2)

    #print solution to the terminal
    print(costMatrix[-1][-1])

    if args.t:
        #backtracking algorithm
        i = len(costMatrix) - 1
        j = len(costMatrix[0]) - 1
        path = ''
        while i > 0 or j > 0:
            if i > 0 and j > 0:
                if args.d:
                    if costMatrix[i-1][j-1]+dWeights[i-1][j-1] == costMatrix[i][j]:
                        path = 'D' + path
                        i -= 1
                        j -= 1
                elif costMatrix[i-1][j] + vWeights[i-1][j] == costMatrix[i][j]:
                    path = 'S' + path
                    i -= 1
                else:
                    path = 'E' + path
                    j -= 1
            elif i == 0:
                path = 'E' + path
                j -= 1
            else:
                path = 'S' + path
                i -= 1

        #print the path
        print(path)



if __name__=="__main__":
    main()