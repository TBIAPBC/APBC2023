#!/usr/bin/env python3

if __name__=="__main__":
    correctInFile = "HelloWorld-test1.in"
    inFileName = input("pls enter the  correct input filename:\n")
    if inFileName == correctInFile:
        with open (inFileName, "r") as f:
            output = f.read()
        print("Hello World!\n",output, sep ='', end='')
    else:
        print("file not accepted")
        
    
    
