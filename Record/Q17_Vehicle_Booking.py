class vehicle:
    def __init__(self,vname,vtype,vprice):
        self.vname = vname
        self.vtype = vtype
        self.vprice = vprice

    def display_details(self):
        print("**Vehicle Details**")
        print("Vehicle Name: ",self.vname)
        print("Vehicle Type: ",self.vtype)
        print("Vehicle Price: ",self.vprice)

c1 = vehicle("Audi","car","1400000")
c1.display_details()           
