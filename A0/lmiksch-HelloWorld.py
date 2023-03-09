import argparse

parser = argparse.ArgumentParser(
                    prog = 'Hello World',
                    description = 'Takes a file as input and the returns hello world + the file content into the command line')


parser.add_argument("input", metavar= "input",  help = "Takes a txt file as input")

args = parser.parse_args()

if args.input == None:
    print("Missing input file. \n Use --input to specify your input")
else:    
    input_file = open(args.input)
    print("Hello World! \b")
    for line in input_file: 
        print(line.strip())
