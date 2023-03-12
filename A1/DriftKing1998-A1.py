import codecs
import sys
from functions import *

# first element after the script will be taken as input
argv = sys.argv
file = argv[-1]
ignore_case = False
print_list = False

# checking for flags
if '-I' in argv:
    ignore_case = True
if '-l' in argv:
    print_list = True

# open file and count words
text = codecs.open(file, 'r', 'utf-8')
word_counts = word_counter(text, ignore_case, print_list)

