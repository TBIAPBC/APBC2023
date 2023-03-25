#!/usr/bin/env python3
import sys
import string
from tabulate import tabulate

""""
Program that reads in a text (file name given on the command line) and counts the total number of words and the number of different
words. 

* If option -I is given, case is ignored 

* If option -l  is present, the program prints a list of words instead only counts.

"""

#function for sorting words from a dictionary based on their occurence and alphabetical order
def sortWords(wordCounts):

    values=list(wordCounts.values())
    values.sort(reverse=True)

    words=list(wordCounts.keys())
    words.sort()

    sol=[]
    for v in values:
        for w in words:
            if wordCounts[w] == v:
                sol.append([w,v])
                words.remove(w)
                break
    return sol

#main function       
if __name__=="__main__":

    if len(sys.argv) > 4:
        print("Too many arguments")
        sys.exit()

    i_Flag = False
    l_Flag = False
    filename = ""
    args = sys.argv[1:]

    #read the arguments(filename, flags)
    for arg in args:
        if arg == "-I":
            i_Flag = True
        elif arg == "-l":
            l_Flag = True
        else:
            filename = arg
    if not filename:
        print("You didn't enter a filename")
        sys.exit()
    
    #open the file, exit if not found
    try:
        with open(filename, "r") as f:
            content = f.read()
    except:
        print(filename, "is not a valid filename")
        sys.exit()
    
    if i_Flag:
        content = content.lower()

    wordCounts = {}

    #create a string of punctuation signs that should be translated into spaces. remove ' from that string (bc of words like don't).
    trans_signs = string.punctuation
    trans_signs = trans_signs.replace("'", "") 
    #translate all punctuation signs into spaces
    translator = str.maketrans(trans_signs, " " * len(trans_signs))
    content = content.translate(translator)
    #now the text can be split
    cList = content.split()

    #fill the dictionary with words -> counts
    for word in cList:
        if word in wordCounts.keys():
            wordCounts[word]+=1
        else:
            wordCounts[word] = 1
      
    #stop here, if -l was not passed as argument
    if not l_Flag:
        print (len(wordCounts), "/",  len(cList))
        sys.exit()
    
    
    sol= sortWords(wordCounts)
    print(tabulate(sol, headers=["words", "counts"]))