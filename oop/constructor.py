#The __init__ method gets invoked as soon as the object is created. It is like the constructor of a class.


class Company:
    # class attribute
    role = "employee"

    # Instance attribute
    def __init__(self, name):
        self.name = name
    
    def change(self, new_name):
        self.name = new_name

# Object instantiation
Halima_obj = Company("Halima")
Sourav = Company("Sourav")

print("My name is " + Halima_obj.name)
Halima_obj.change("Othmane")
print("My name is " + Halima_obj.name)


# Accessing class attributes
print("Sakshi is an {}".format(Halima_obj.__class__.role))
print("Sourav is also an {}".format(Sourav.__class__.role))

# Accessing instance attributes
print("My name is {}".format(Halima_obj.name))
print("My name is {}".format(Sourav.name))
    
    


class Product:
    
    def __init__(self, nom, qnt, price):
        self.nom = nom
        self.qnt = qnt
        self.price = price
        
    def somme_totale(self):
        return self.qnt*self.price
    
class User:
    def __init__(self, username, passwd):
        self.username = username
        self._passwd = passwd
        
    
usr = User("halima", "ldjhlsdf")
print(usr.passwd)