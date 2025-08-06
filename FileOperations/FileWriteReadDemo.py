f = open("test.txt","w+") #open the file using read and write modes

for i in range(0,3):
    f.write(f"This is line {i+1}\n") #printing lines

f.close # closing the file

# Printing the contents from the file
f.open("test.txt","r")
content = f.read()
print(content)