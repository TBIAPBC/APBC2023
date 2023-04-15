"""
Notes after finishing:
- Constructing weighted edges by a dictionary of tuple of tuples is not necessary, rather use a scoring matrix next time.
- Backtracking: Dont backtrack from scratch after the DP has finished, rather create a backtrack matrix that is generated during the DP matrix run

___________________________________ DYNAMIC PROGRAMMING ______________________________________
how the algorithms works:
initiating the source (node in left top corner) with 0 I fill the other node_weights as follows:
- I consider my node of interest as my InputHV node and all predecessor node_weights (which project 
  an edge towards my InputHV node) as output node_weights.
- The value of my InputHV node is the maximum value of each output node value + it´s edge weight
- Since my graph is already topologically ordered I can loop row after row until I reach the
  sink (node in the hori bottom corner) which harbors my final maximum value
- an edge is denoted by, e.g. from source node to next hori node by [(0,0),(0,1)]
- for the weight I could apply a dictionary
_______________________________________________________________________________________________
"""
import sys

def InputHV(file):
    file = open(file).readlines()
    file = [i.strip() for i in file]
    
    """filtering only the lines that contain values of interest/street values ->"""
    vert = [] # vertical (north-south) streets (edge weights)
    hori = [] # horizontal streets
    switch = 0 # switch from storing vertical streets to storing horizontal streets, depending how many numbers are in the current line of the file (difference of the 2 categories is the length/dimension)
    for i in file:
        if len(i) != 0 and i[0].isnumeric(): 
            if switch == 0:
                switch = len(i.split()) # switch becomes the length of the north-south values
            if switch != len(i.split()): # when the west-east values are reached the number of numbers in the corresponding line changes
                hori.append(i.split())
            else:
                vert.append(i.split())

    vert = zip(*vert) # transpose for easier handling

    vert = [[float(j) for j in i] for i in vert]
    hori = [[float(j) for j in i] for i in hori]
    return vert, hori

def HighScoreHV(file):
    vert, hori = InputHV(file) # weight values as 2D array (list)

    # matrix size measures
    heigth = len(hori); broadth = len(vert)
    # print("heigth:", heigth, "broadth:", broadth, "\n")

    # print("vertical streets:"); [print(i) for i in vert]
    # print("\nhorizontal streets:"); [print(i) for i in hori]; print()
    
    # # matrix for index values
    indices = [[]for i in range(heigth)]
    for row in range(heigth):
        for col in range(broadth):
            indices[row].append((row,col))
    # print("indices:"); [print(i) for i in indices]; print()

    # # dictionary for set of edge_weights with weight 
    edge_weights = {}
    for row in range(heigth):
        for col in range(broadth-1):
            edge_weights[(indices[row][col], indices[row][col+1])] = hori[row][col]

    for row in range(broadth):
        for col in range(heigth-1):
            edge_weights[(indices[col][row], indices[col+1][row])] = vert[row][col]
    # print("edge_weights:"); [print(i, edge_weights[i]) for i in edge_weights]; print()

    # # matrix for node values    
    node_weights = {}
    for i in indices: # initialized with value 0 each
        for j in i:
            node_weights[j] = 0

    edge_weights_keys = list(edge_weights.keys())
    for row in range(heigth): # iterating through every element of the (imaginary) node matrix
        for col in range(broadth):
            max = 0
            if row==0 and col == 0: node_weights[(row,col)] = 0 # value of the grids source node remains zero for initiation
            else:
                for edge in edge_weights_keys: # edge corresponds to a tuple of tuples (coordinates that define the edge)
                    if edge[1] == (row,col): # edge_weights which 2nd tuple (all edge_weights that target the current node/all incoming edge_weights)
                        if edge_weights[edge] + node_weights[edge[0]] > max: # for each incoming edge we evaluate the sum of its weight and the weight of its starting node
                            max = edge_weights[edge] + node_weights[edge[0]] # from all those candidates (in our case maximal 2) the maximum is obtained
                node_weights[(row,col)] = max
                           
    # print("node_weights:"); [print(i, node_weights[i]) for i in node_weights]; print()

    if "-t" in arg:
        path=[indices[-1][-1]] #initiate with final node
        letters = ""
        while path[-1] != (0,0):
            cur_ind = path[-1] # current node index
            up_ind = (cur_ind[0]-1, cur_ind[1]) # index of node above current .node
            left_ind = (cur_ind[0], cur_ind[1]-1)
            if cur_ind[0]>0 and node_weights[cur_ind] - edge_weights[up_ind,cur_ind] == node_weights[up_ind]:
                path.append(up_ind)
                letters = 'S' + letters
            elif cur_ind[1]>0 and node_weights[cur_ind] - edge_weights[left_ind,cur_ind] == node_weights[left_ind]:
                path.append(left_ind)
                letters = 'E' + letters  

        return node_weights[(heigth-1, broadth-1)], letters
    
    else:
        return node_weights[(heigth-1, broadth-1)]

def InputHVD(file):
    file = open(file).readlines()
    file = [i.strip() for i in file]

    vert=[]; hori=[]; diag=[]
    data = [vert,hori,diag]
    switch = 0
    for i in range(len(file)):
        if len(file[i]) > 0 and file[i][0].isnumeric():
            data[switch].append(file[i].split())
            if not file[i+1][0].isnumeric() and switch < 3:
                switch+=1

    vert = zip(*data[0])

    vert = [[float(j) for j in i] for i in vert]
    hori = [[float(j) for j in i] for i in data[1]]
    diag = [[float(j) for j in i] for i in data[2]]

    return vert,hori,diag

def HighScoreHVD(file):
    vert, hori, diag = InputHVD(file)
    # print("vert:"), [print(i) for i in vert], print()
    # print("hori:"), [print(i) for i in hori], print()
    # print("diag:"), [print(i) for i in diag], print()

    heigth = len(hori); broadth = len(vert); diagonal = len(diag)
    # print("heigth:", heigth,"\nbroadth:", broadth,"\ndiagonal:", diagonal)

    indices = [[]for i in range(heigth)]
    for row in range(heigth):
        for col in range(broadth):
            indices[row].append((row,col))
    # print("\nindices (2D list):"); [print(i) for i in indices]

    edge_weights = {}
    for row in range(heigth):
        for col in range(broadth-1):
            edge_weights[(indices[row][col], indices[row][col+1])] = hori[row][col]

    for col in range(broadth):
        for row in range(heigth-1):
            edge_weights[(indices[row][col], indices[row+1][col])] = vert[col][row]

    for row in range(diagonal):
        for col in range(len(diag[row])):
            edge_weights[(indices[row][col], indices[row+1][col+1])] = diag[row][col]
    # print("\nedge_weights (dictionary):"); [print(i, edge_weights[i]) for i in edge_weights]; print()
    
    node_weights = {}
    for i in indices:
            for j in i:
                node_weights[j] = 0

    edge_weights_keys = list(edge_weights.keys())

    for row in range(heigth):
        for col in range(broadth):
            max = 0
            if row == 0 and col == 0: node_weights[(row,col)] = 0
            else:
                for edge in edge_weights_keys:
                    if edge[1] == (row,col):
                        if edge_weights[edge] + node_weights[edge[0]] > max:
                            max = edge_weights[edge] + node_weights[edge[0]]
                node_weights[(row,col)] = max
    # print("node_weights (dictionary):"); [print(i, node_weights[i]) for i in node_weights]; print()

    if "-t" in arg:
        path=[indices[-1][-1]] #initiate with final node
        letters = ""
        while path[-1] != (0,0):
            cur_ind = path[-1] # current node index
            up_ind = (cur_ind[0]-1, cur_ind[1]) # index of node above current node
            diag_ind = (cur_ind[0]-1, cur_ind[1]-1)
            left_ind = (cur_ind[0], cur_ind[1]-1)
            if cur_ind[0]>0 and node_weights[cur_ind] - edge_weights[up_ind,cur_ind] == node_weights[up_ind]:
                path.append(up_ind)
                letters = 'S' + letters
            elif cur_ind[0]>0 and cur_ind[1]>0 and node_weights[cur_ind] - edge_weights[diag_ind,cur_ind] == node_weights[diag_ind]:
                path.append(diag_ind)
                letters = 'D' + letters
            elif cur_ind[1]>0 and node_weights[cur_ind] - edge_weights[left_ind,cur_ind] == node_weights[left_ind]:
                path.append(left_ind)
                letters = 'E' + letters    

        return node_weights[(heigth-1, broadth-1)], letters
    
    else:
        return node_weights[(heigth-1, broadth-1)]

                
def main():
    global arg 
    arg = sys.argv
    file = arg[1]
    
    if "-d" in arg:
        if "-t" in arg:
            sink_node, path = HighScoreHVD(file)
            print(sink_node); print(path)
        else:
            sink_node = HighScoreHVD(file)
            print(sink_node)
    else:
        if "-t" in arg:
            sink_node, path = HighScoreHV(file)
            print(sink_node); print(path)

        else:
            sink_node = HighScoreHV(file)
            print(sink_node)


    """
    To-Do:
    - change main such that input file calls either HV or HDV, if not -d -> HV if -d HV+HVD
    - too slow
    """




    print("\nfinished.")
if __name__ == "__main__":
    main()
