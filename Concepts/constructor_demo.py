class student():
    def __init__(self,name,roll_no,course):
        self.name = name
        self.roll_no = roll_no
        self.course = course

    def display(self):
        print("****Student Details****")
        print(f"Name is: {self.name}")
        print(f"Roll NO: {self.roll_no}")
        print(f"Course: {self.course}")

st1 = student("Agus","101","MSCCS")
st1.display()