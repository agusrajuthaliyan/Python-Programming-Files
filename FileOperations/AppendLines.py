import os
filepath = input("Enter the file path: ")

if os.path.exists(filepath):
    with open(filepath,"a+") as f:
        for i in range(0,2):
            f.write(f"This is new line {i+1}\n")
    f = open("test.txt")
    content = f.read()
    print(content)