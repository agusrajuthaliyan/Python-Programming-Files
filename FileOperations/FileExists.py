import os
filepath = input("Enter the file path: ")

if os.path.exists(filepath):
    print('The file exists!')
    print("The contents of the file are \n")
    with open(filepath,"r") as f:
        contents = f.read()
        print(contents)

else:
    print('The file doesnt Exist!')
