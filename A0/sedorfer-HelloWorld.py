import sys

with open(f"{sys.argv[1]}", "r") as f:
    print(f"Hello World!\n{f.read()}")
