def find_unique_number(nums):
    unique = 0
    for num in nums:
        unique ^= num
    return unique

def main():
        length = int(input("Enter the number of elements: "))
        elements = []
        for i in range(length):
            elem = int(input(f"Enter element {i + 1}: "))
            elements.append(elem)
        result = find_unique_number(elements)
        print(f"The unique number is: {result}")

main()