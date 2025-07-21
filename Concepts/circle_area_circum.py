class circle():
    def __init__(self,radius):
        self.radius = radius

    def get_area(self):
        area = (22/7)*self.radius*self.radius
        print(f"The area of the circle is: {area}")
    
    def get_circumference(self):
        circum = 2*(22/7)*self.radius
        print(f"The circumference of the circle is: {circum}")

cir1 = circle(3)
cir1.get_area()
cir1.get_circumference()