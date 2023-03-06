#!/usr/bin/env python3

if __name__=="__main__":
    
    inFileName = input("pls enter the input filename:\n")
    with open (inFileName, "r") as f:
        output = f.read()
    print("Hello World!\n",output, sep ='', end='')
    
    
