import sys

# To run this script in your command line enter python3 sedorfer-HelloWorld.py HelloWorld-test1.in
# This program accepts a single file name as a command line argument and prints its content together with a greeting

with open(f"{sys.argv[1]}", "r") as f:              # opens the file and closes it after completion
    print(f"Hello World!\n{f.read()}")              # prints a greeting and the file content
