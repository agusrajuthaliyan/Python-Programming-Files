def odd_even(num):
    if num%2==0:
        print(num,"is Even!")
    else:
        print(num,"is Odd!")

def armstrong(num):
    sumsqr = 0
    numog = num
    while num:
        rem = num%10
        num = int (num/10)
        sumsqr = sumsqr + (rem**3)
    if numog == sumsqr:
        print("The number",numog,"is an Armstrong!")
    else:
        print("The number",numog,"is not an Armstrong, the result is: ",sumsqr)
def prime(num):
    if num > 1:
        count = 0
        for i in range(2,num):
            if num%i == 0:
                count+=1
            else:
                continue
        if count==0:
            print(num,"is prime number!")
        elif count > 0:
            print(num,"is not prime!")
    elif num == 1:
        print("The number",num,"is neither prime nor composite!")
    elif num == 0:
        print("The number is zero!")
    else: 
        print("Negetive number!")

def perfect(num):
    sum = 0
    for i in range(1,num):
        if num%i == 0:
            sum+=i
    if sum == num:
        print("The number",num,"is a perfect number!")
    else:
        print("The number",num,"is not a perfect number, with the divisor sum: ",sum)

def main():
    num = int(input("Enter a number: "))
    odd_even(num)
    armstrong(num)
    prime(num)
    perfect(num)
main()