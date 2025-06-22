all_attendees = []
aids_attendees = []
cybsec_attendees = []
both_attendees = []

def eventreg():
    person = input("Enter your name: ")
    print("\n1. Join AI & Data Science Event")
    print("2. Join Cyber Security Event")
    print("3. Join Both Events\n")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        aids_attendees.append(person)
    elif choice == 2:
        cybsec_attendees.append(person)
    elif choice == 3:
        both_attendees.append(person)
    else:
        print("Wrong Input!")
    all_attendees.append(person)

def list_unique():
    print(set(aids_attendees) | set(cybsec_attendees) | set(both_attendees))

def list_both():
    print(both_attendees)

def onlyAIDS():
    print(set(all_attendees) & set(aids_attendees))

def onlyCYBSEC():
    print(set(all_attendees) & set(cybsec_attendees))

def main():
    while True:
        print("\n1. Event Registration")
        print("2. List Unique Attendees")
        print("3. List Participants attending both events")
        print("4. List Participants for AI & Data Science only")
        print("5. List Participants for Cyber Security only")
        print("0. Exit!\n")
        choice = int(input("Enter your choice (0-5): "))
        if choice == 1:
            eventreg()
        elif choice == 2:
            list_unique()
        elif choice == 3:
            list_both()
        elif choice == 4:
            onlyAIDS()
        elif choice == 5:
            onlyCYBSEC()
        elif choice == 0:
            break
        else:
            print("Wrong Input!")
main()