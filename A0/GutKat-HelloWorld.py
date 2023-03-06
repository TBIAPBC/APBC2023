import argparse
import os

parser = argparse.ArgumentParser(description='A0 - Warm up assignment: Hello World')
parser.add_argument('-i', '--input', type=str, help='the input file')
args = parser.parse_args()

with open(args.input, "r") as f:
    content = f.read()

print("Hello World!")
print(content)
