import argparse

parser = argparse.ArgumentParser(
                    prog = 'Hello World',
                    description = 'Takes a file as input and the returns hello world + the file content into the command line')


parser.add_argument("--input", metavar= "i",  help = "Takes a txt file as input")

args = parser.parse_args()


input_file = open(args.input)
print("Hello World! \b")
for line in input_file: 
    print(line.strip())
