def process_string(str):
    upperCase(str)
    lowerCase(str)
    print("The length of the string is: ",len(str))
    print("The Reverse is: ",rev(str))
    palindrome(str)

def upperCase(str):
    print(str.upper())

def lowerCase(str):
    print(str.lower())

def rev(str):
    return str[::-1]
    
def palindrome(str):
    str1 = str.lower()
    if rev(str.lower()) == str1:
        print("The string is a palindrome!!!")
    else:
        print("Not palindrome")
        
def main():
    str = input("Enter a string: ")
    process_string(str)

main()