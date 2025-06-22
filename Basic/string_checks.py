def check_substr():
    str = input("Enter a string: ")
    substr = input("Now enter the substring: ")
    if substr in str:
        print("The sub-string '",substr,"' is present in the string: ",str)
    else:
        print("The substring is not in the string: ")

def count_occurances():
    str = input("Enter a string: ")
    char = input("Enter the character: ")
    count = 0
    for i in range(0,len(str)):
        if char == str[i]:
            count+=1
        else:
            continue
    print(f"The character has {count} occurances!")

def replace_substr():
    str = input("Enter the string: ")
    str1 = input("Enter the substring to be replaced: ")
    str2 = input("Enter the substring to replace with: ")
    print(str.replace(str1,str2))

def tocaps():
    str = input("Enter the string: ")
    print(str.upper())


def main():
    while True:
        print("1. Check if string is a substring of another")
        print("2. Count Character Occurances")
        print("3. Replace a substring with another substring")
        print("4. Convert to capital")
        print("0. Exit!")
        choice = int(input("Enter a choice: (0-4): "))
        if choice == 0:
            break
        elif choice == 1:
            check_substr()
        elif choice == 2:
            count_occurances()
        elif choice == 3:
            replace_substr()
        elif choice == 4:
            tocaps()
        else:
            break

main()