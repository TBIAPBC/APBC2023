import sys
arg = sys.argv

try:
    file = open(arg[1])
    print("Hello World!")
    print(file.read(), end="")
except:
    print("No such file in directory")