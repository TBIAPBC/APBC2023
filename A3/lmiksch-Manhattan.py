import argparse
import numpy as np

def input_parser(input_file,diag = False):
    """Parses the input file. Ignores lines starting with #
    
    Args: 
        input_file(str): Name of the input file
        diag(boolean): Flag if command -d has been added in the command line

    Returns:
        A matrix corresponding to the weighted directions
    
    """

    #parsing input creates for every direction a matrix
    down_block = []
    right_block = []
    diag_block = []
    


    with open(args.input) as input: 
        lines = input.readlines()
        raw_input = []
        for line in lines:
        
            if line[0] != "#" and len(line) != 0: 
                raw_input.append(line.strip().split())
    
    raw_input = [sublist for sublist in raw_input if sublist]

    i = 0
    x = 0
    #Each Direction is indicated by x. If it recognizes that the directions matrix is filled it increases x. 
    #There is probably a better solution to this
    while x != 3:
        if x == 0:
            if len(raw_input[i + 1]) < len(raw_input[i]):
                x += 1 
            down_block.append(raw_input[i])
            i += 1
          
        elif x == 1:
            right_block.append(raw_input[i])
            i += 1
            if len(right_block) == len(down_block)+1:
                x += 1 
        elif x == 2 and diag == False:
            break
        elif diag == True and x == 2:
            diag_block.append(raw_input[i])
            i += 1 

         
        if i == len(raw_input):
            break    
   
    return(down_block,right_block,diag_block)

def init_matrix(down_block, right_block):
    """Creates a matrix based on the grid size derived from the input and fills the first row and column based on the weights.
    """

    grid_size = (len(right_block)),len(down_block[0])
    print(grid_size)
    
    #initialize matrix
    
    matrix = np.zeros(grid_size, dtype=float)
    dir_matrix = [["" for x in range(grid_size[1])] for z in range(grid_size[0])]
    
    #Fill first row
    for x in range(1, grid_size[1]):
        
        matrix[0][x] = matrix[0][x-1] + float(right_block[0][x-1]) 

        dir_matrix[0][x] = dir_matrix[0][x-1] + "E"

    # Fill first column
    for x in range(1, grid_size[0]):
        matrix[x][0] = matrix[x-1][0] + float(down_block[x-1][0])
        dir_matrix[x][0] = dir_matrix[x-1][0] + "S"
       
    return matrix, dir_matrix



def fill_matrix(down_block,right_block,diag_block, matrix,dir_matrix):
    """Fill the matrix based on the rules in the readme and saves the scores in a matrix. It also saves the paths in each cell. 

        Args: 
            down_block(list): List from input
            right_block(list): List from input
            diag_block(list): List from input None if -d flag is not active
            matrix(list): List which represents the socring matrix 
            dir_matrix(list): Saves the direction from which the highest score comes from 

        Returns:
            matrix(list): List of lists containing the max score in each cell
            dir_matrix(list): List where each cell entry has the optimal path to arrive at this cell with the highest score.  

        
    """
    grid_size = (len(right_block),len(down_block[0]))
    #fill matrix row by row 

    for row in range(1,grid_size[0]):
        
        for column in range(1,grid_size[1]):
            diag = 0
            right = matrix[row][column-1] + float(right_block[row][column-1])
            down = matrix[row-1][column] + float(down_block[row-1][column])
            
            if len(diag_block) != 0:
                diag = matrix[row-1][column-1] + float(diag_block[row-1][column-1])
                

            if right > down and right > diag: 
                matrix[row][column] = right
                dir_matrix[row][column] = dir_matrix[row][column-1] + "E"
            elif diag > right and diag > down:
                matrix[row][column] = diag
                dir_matrix[row][column] = dir_matrix[row-1][column-1] + "D"
            elif down >= right and down >= diag: 
                matrix[row][column] = down 
                dir_matrix[row][column] = dir_matrix[row-1][column] + "S"
            elif down == right or down == diag:
                matrix[row][column] = down 
                dir_matrix[row][column] = dir_matrix[row-1][column] + "S"
    return(matrix,dir_matrix)


def traceback(matrix,row,column,path,down_block,right_block,diag_block): 
    """Traces back the optimal path and returns the path. Tried to also implement a traceback function. This does not work with HVD2 (too many recursions)
    """

    if row == 0 and column == 0:
        path.reverse()
        return path  
    if row == 0:
        while column != 0:
            path.append("E")
            column += -1
        path.reverse()
        return path
    
    if column == 0:
        while row != 0:
            path.append("S")
            row += 1
        path.reverse()
        return path

          

    diag = 0
    down = matrix[row - 1][column] + float(down_block[row-1][column])
    right =  matrix[row][column-1] + float(right_block[row][column-1])
    
    if len(diag_block) != 0: 
        diag = matrix[row-1][column-1] + float(diag_block[row-1][column-1])

    if right > down and right > diag:         
        path.append("E")
        column += -1

    elif diag > right and diag > down:
        path.append("D")
        row += -1
        column += -1
    elif down >= right and down >= diag: 
        path.append("S")
        row += -1
    elif down == right or down == diag:
        path.append("S") 
        row += -1
    
    return traceback(matrix,row,column,path,down_block,right_block,diag_block)



                
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                            prog='Manhatten solver',
                            description='First argument needs to be a txt file with the input. Inputs must have the order down,right,diagonal. # will not be read into the file.',
                            )

    parser.add_argument("input",help="Input File")
    parser.add_argument("-t","--track", help= "Additionally displays the best path",action="store_true")
    parser.add_argument("-d","--diagonal", help="Allows input files with diagonals",action="store_true")

    args = parser.parse_args()
    
    down_block,right_block, diag_block = input_parser(args.input,args.diagonal)
    grid_size = (len(right_block),len(down_block[0]))

    matrix, dir_matrix = init_matrix(down_block,right_block)

    matrix, dir_matrix = fill_matrix(down_block,right_block,diag_block,matrix,dir_matrix)


    #workaround to display resulting integers as ints
    final_weight = str(matrix[-1][-1]).split(".")
    if final_weight[1] == "0":
        print(final_weight[0])
    else:
        print(format(matrix[-1][-1],".2f"))

    if args.track:
        path = []
        print(dir_matrix[-1][-1])

        #uncomment to also use the traceback function does not work with HVD2 since it hits the recursion limit
        #final_path = traceback(matrix,grid_size[0]-1,grid_size[1]-1,path,down_block,right_block,diag_block)
        #print("".join(final_path))



