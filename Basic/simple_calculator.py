def addition(a,b):
    return print(f"The addition of {a}+{b} is: ",a+b)

def subtraction(a,b):
    return print(f"The subtraction of {a}-{b} is: ",a-b)

def multiplication(a,b):
    return print(f"The multiplication of {a}*{b} is: ",a*b)

def division(a,b):
    return print(f"The division of {a}/{b} is: ",a/b)

def main():
    while True:
        a = int(input("Enter the value of a: "))
        b = int(input("Enter the value of b: "))
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("0. Exit")
        choice = int(input("Enter your choice(0-4): "))
        if choice == 1:
            addition(a,b)
        elif choice == 2:
            subtraction(a,b)
        elif choice == 3:
            multiplication(a,b)
        elif choice == 4:
            division(a,b)
        elif choice == 0:
            break
        else:
            print("Wrong input!")
main()