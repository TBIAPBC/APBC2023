import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input", metavar="input", type=str, help="enter your input")
args = parser.parse_args()

input = args.input

with open (input, "r") as content:
    print("Hello World!\n")
    print(content.read().rstrip("\n"))
