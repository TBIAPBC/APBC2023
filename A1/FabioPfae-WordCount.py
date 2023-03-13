"""
- read text file as command line argument
- count total number of words
- count number of different words
- on request print list of words (all words)
- if option -I | ignore case (convert upper to lower case)
- if option -l | list of words with frequency 
        - without printing total/different words
        - sort primary by frequency, secondary by alphabet
        - separate by tab
- ignore non letter symbols
- must accept both options at the same time
"""

import sys
arg = sys.argv
print(arg)
letters_lower = "abcdefghijklmnopqrstuvwxyzäöü" + "ß"
letters_upper = letters_lower.upper() + "ß"
letters = letters_upper + letters_lower

# creates array of unsorted words
text = open(arg[1]).read()
words = []
word = ""
flag = False

if "-I" in arg:
    text = text.lower()

for i in range(len(text)):
    if text[i] in letters:
        word = word+text[i]
        flag = True
    else:
        if flag:
            words.append(word)
            word = ""
            flag = False

# counts frequency of words and stores in dictionary
dic_unsorted = {}
dic = {}
max_val = 0
for i in words:
    if i not in dic_unsorted:
        dic_unsorted[i] = 1
    else:
        dic_unsorted[i] = dic_unsorted[i]+1

#identify the highest word frequency
for i in dic_unsorted:
    if dic_unsorted[i] > max_val:
        max_val = dic_unsorted[i]

#max frequency stored for later
temp = max_val

#sorted dictionary by frequency but not alphanumerically
while(max_val >= 1):
    for i in dic_unsorted:
        if dic_unsorted[i] == max_val:
            dic[i] = max_val
    max_val = max_val -1

#transforming frequency sorted dictionary into 2D array for easier alphanumerical sorting.
#subarray = words sharing the same freuqency
max_val = temp
arr = [[]]
ind = 0
while(max_val >= 1):
    for i in dic:
        if dic[i] == max_val and max_val in list(dic.values()):
            arr[ind].append(i + (" ")*(19-len(i)) + str(dic[i]))
    max_val -= 1
    if max_val in list(dic.values()):
        arr.append([])
        ind += 1

#alphanumerical sorting of 2D array via bubble-sort
for i in range(len(arr)):
    for j in range(len(arr[i])-1):
        for k in range(len(arr[i])-j-1):
            if arr[i][k+1] < arr[i][k]:
                arr[i][k+1], arr[i][k] = arr[i][k], arr[i][k+1]

# command line request wether printed output shall be 
# - total bzw. unique number of words
# - or list of words with frequency
if "-l" not in arg:
    print(len(dic), " / ", len(words))
else:
    for i in arr:
        for j in i:
            print(j)


