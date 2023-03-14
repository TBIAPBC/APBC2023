# python3, input.in, --list, --Ignore
import argparse
import re

# configure command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("input", metavar="input", type=str, help="enter your input")
#-I ignores upper case
parser.add_argument("-I", "--Ignore", action="store_true")
#-l list words
parser.add_argument("-l", "--list", action="store_true")
args = parser.parse_args()

# set input and output and make empty dictionary and count
input = args.input
my_output = "".join(input.split(".")[:-1]) + ".out"
d = dict()
count = 0

# open input, read line wise and safe words into dictionary
with open(input, "r") as content:
    for line in content:
        # remove leading spaces and newline character
        line = line.strip()

        # make all lower case if -I is stated in command line
        if args.Ignore:
            line = line.lower()

        # remove special characters
        noSpecChar = re.sub("[^A-Za-z]", " ", line)

        # split line to words
        words = noSpecChar.split()

        # fill dictionary
        for word in words:
            count += 1
            if word in d:
                d[word] += 1
            else:
                d[word] = 1

with open(my_output, "w") as my_out:

    # list words when -l is stated in command line
    if args.list:
        # sort keys alphabetically
        sort_dict = sorted(d.keys(), key=lambda x:x)
        # sort dictionary by values from biggest to smalles and print to output file
        for w in sorted(sort_dict, key=d.get, reverse=True):
            print(w, "\t", d[w], file=my_out)
    else:
        print(len(d), "/", count, file=my_out)