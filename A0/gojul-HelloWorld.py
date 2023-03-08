inp = ("HelloWorld-test1.in")

with open (inp, "r") as content:
    print("Hello World!\n")
    print(content.read().rstrip("\n"))
