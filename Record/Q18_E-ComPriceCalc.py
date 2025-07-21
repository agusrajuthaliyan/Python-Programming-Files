items = {}

class Cart:
    total=0
    def __init__(self,price,quantity):
        self.price = price
        self.quantity = quantity

    def add_item(self):
        items["price"] = self.price
        items["quantity"] = self.quantity
        Cart.total =Cart.total+self.price*self.quantity

    @classmethod
    def get_total(cls):
       # cls.total = items["price"] * items["quantity"]
        print("The total price is: ",cls.total)

c1 = Cart(120,2)
c2 = Cart(110,3)
Cart.add_item(c1)
Cart.add_item(c2)
Cart.get_total()