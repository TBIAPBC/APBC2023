import argparse
import os

parser = argparse.ArgumentParser(description='A0 - Warm up assignment: Hello World')
parser.add_argument('-i', '--input', type=str, help='the input file')
args = parser.parse_args()

output =os.path.splitext(args.input)[0] + ".out"
print(args.input, output)
with open(args.input, "r") as f:
    content = f.read()

with open(output, "w") as f:
    f.write("Hello World! \n")
    f.write(content)
