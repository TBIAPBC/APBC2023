if __name__=="__main__":
    inp = input("Enter your file name: ")

    with open (inp, "r") as content:
        print("Hello World!\n")
        print(content.read().rstrip("\n"))
