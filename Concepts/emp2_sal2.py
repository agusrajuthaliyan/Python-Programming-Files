class Employee2:
    def __init__(self,name,emp_id,salary):
        self.name = name
        self.emp_id = emp_id
        self.salary = salary
    
    def salary_calc(self):
        gross = self.basic_pay + (0.2*self.basic_pay) + (0.1 *self.basic_pay)
        print(f'Basic salary is: {salary}')
        print(f'Gross salary is: {gross}')

c = Employee2('Arjun','A1','12000')
c.salary_calc()