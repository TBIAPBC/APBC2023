import sys

# reading in the file given in the command line
opened_test = open(sys.argv[1], 'r')

# printing out 'Hello World'
print(f'Hello World')
# printing out each line in the input separately
for line in opened_test:
    print(line.rstrip())
#test
