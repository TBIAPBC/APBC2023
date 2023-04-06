import argparse

def input_parser(input_file,diag = False):
    #parsing input creates for every direction a matrix
    down_block = []
    right_block = []
    diag_block = []
    input_type = 0
    new_block = True
    with open(input_file) as input: 
        lines = input.readlines()
        raw_input = []

        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue


            if line.startswith("#") and new_block == False:
                continue
                
            if not line.startswith("#") and input_type == 1:
                down_block.append(line.strip().split())
                new_block = True

            if not line.startswith("#") and input_type == 2:
                right_block.append(line.strip().split())    
                new_block = True

            if diag == True and not line.startswith("#") and input_type == 3:
                diag_block.append(line.strip().split())
                new_block = True
            
            if line.startswith("#") and new_block == True:
                input_type += 1 
                new_block = False
    
    return(down_block,right_block,diag_block)









def init_matrix(down_block,right_block):

    grid_size = (len(down_block[0]),len(right_block))

    #initialize matrix
    matrix = [[0 for x in range(grid_size[0])] for z in range(grid_size[1])]
    dir_matrix = [["" for x in range(grid_size[0])] for z in range(grid_size[1])]

    #Fill first row
    for x in range(1,len(matrix[0])):
        matrix[0][x] = matrix[0][x-1] + float(right_block[0][x-1]) 
        dir_matrix[0][x] = dir_matrix[0][x-1] + "E"

    # Fill first column
    for x in range(1,len(matrix)):
        matrix[x][0] = matrix[x-1][0] + float(down_block[x-1][0])
        dir_matrix[x][0] = dir_matrix[x-1][0] + "S"

    return matrix,dir_matrix



def fill_matrix(down_block,right_block,diag_block, matrix,dir_matrix):
    """Fill the matrix based on the rules in the readme and saves the scores in a matrix. 

        Args: 
            down_block(list): List from input
            right_block(list): List from input
            diag_block(list): List from input None if -d flag is not active
            matrix(list): List which represents the socring matrix 
            dir_matrix(list): Saves the direction from which the highest score comes from 

        Returns:
            matrix(list): List of lists containing the max score in each cell 

        Todo:
            Write diag rule 
    """
    grid_size = (len(down_block[0]),len(right_block))
    #fill matrix row by row 

    for row in range(1,grid_size[0]):
        
        for column in range(1,grid_size[1]):
            
           # need to 
            diag = 0
            right = matrix[row][column-1] + float(right_block[row][column-1])
            down = matrix[row-1][column] + float(down_block[row-1][column])
            
            if len(diag_block) != 0:
                diag = matrix[row-1][column-1] + float(diag_block[row-1][column-1])
                


            #print(max(right,down))
            if right > down and right > diag: 
                matrix[row][column] = right
                dir_matrix[row][column] = dir_matrix[row][column-1] + "E"
            elif diag > right and diag > down:
                matrix[row][column] = diag
                dir_matrix[row][column] = dir_matrix[row-1][column-1] + "D"
            elif down > right and down > diag: 
                matrix[row][column] = down 
                dir_matrix[row][column] = dir_matrix[row-1][column] + "S"
            elif down == right or down == diag:
                matrix[row][column] = down 
                dir_matrix[row][column] = dir_matrix[row-1][column] + "S"
    return(matrix,dir_matrix)

'''
def traceback(matrix): 
    path = []

    for row in range(grid_size[0],0,-1):
        for column in range(grid_size[1],0,-1):
            down = matrix[row - 1][column] + float(down_block[row-1][column])
            right =  matrix[row][column-1] + float(right_block[row][column-1])
'''
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

    matrix, dir_matrix = init_matrix(down_block,right_block)

    matrix, dir_matrix = fill_matrix(down_block,right_block,diag_block,matrix,dir_matrix)

    print(round(matrix[-1][-1],4))

    if args.track:
        print(dir_matrix[-1][-1])
    



