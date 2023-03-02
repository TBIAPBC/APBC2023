if __name__=="__main__":
    
    inFileName = input("pls enter the input filename:\n")
    print("Hello World!")
    with open (inFileName, "r") as f:
        for line in f:
            print(line)
    