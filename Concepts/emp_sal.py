class Employee():
    def __init__(self,emp_id,name,basic_pay):
        self.emp_id = emp_id
        self.name = name
        self.basic_pay = basic_pay
    
    def calculate_salary(self):
        gross = self.basic_pay + (0.2*self.basic_pay) + (0.1 *self.basic_pay)
        print(f"The Basic Salary is: {self.basic_pay}")
        print(f"The Calculated Salary is: {gross}")

emp1 = Employee("101","Sundar",12000)
emp1.calculate_salary()