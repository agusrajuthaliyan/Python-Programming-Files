def lowercase(str):
    print("Lower Case: ",str.lower())

def uppercase(str):
    print("Upper Case: ",str.upper())

def strlen(str):
    print("The length of the string is: ",len(str))

def stringrev(str):
    return str[::-1]

def palindrome(str):
    if stringrev(str.lower()) == str.lower():
        print("The string is a palindrome!")
    else:
        print("The string is not a palindrome!")

def main():
    str = input("Enter a string: ")
    lowercase(str)
    uppercase(str)
    strlen(str)
    rev = stringrev(str)
    print("Reverse is: ",rev)
    palindrome(str)

main()