def createEntry(phonebook):
    name = input("Enter the name: ")
    phone = input("Enter the Phone No: ")
    phonebook[name] = phone

def updateEntry(phonebook):
    person = input("Enter the name to change the phone number: ")
    if person in phonebook:
        newphone = input("Enter the new phone no: ")
        phonebook[person] = newphone

def deleteEntry(phonebook):
    person = input("Enter the name to delete the entry: ")
    if person in phonebook:
        del phonebook[person]
        print(f"Entry for {person} deleted.")
    else:
        print(f"No entry found for {person}.")
    

def viewEntry(phonebook):
    print(phonebook)

    
def searchEntry(phonebook):
    person = input("Enter the person to search: ")
    if person in phonebook:
        print(f"{person} is present")
    else:
        print(f"{person} is not in the phonebook entry!")

def main():
    phonebook = {}
    while True:
        print("1. Create Entry")
        print("2. Update Entry")
        print("3. Delete Entry")
        print("4. Search Entry")
        print("5. View Entries")
        print("0. Exit!")
        choice = int(input("Enter your choice (0-4): "))
        if choice == 1:
            createEntry(phonebook)
        elif choice == 2:
            updateEntry(phonebook)
        elif choice == 3:
            deleteEntry(phonebook)
        elif choice == 4:
            searchEntry(phonebook)
        elif choice == 5:
            viewEntry(phonebook)
        else:
            break
main()