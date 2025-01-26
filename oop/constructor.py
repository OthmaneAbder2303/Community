#The __init__ method gets invoked as soon as the object is created. It is like the constructor of a class.


class Company:
    # class attribute
    role = "employee"

    # Instance attribute
    def __init__(self, name):
        self.name = name

# Object instantiation
Sakshi =  Company("Sakshi")
Sourav = Company("Sourav")

# Accessing class attributes
print("Sakshi is an {}".format(Sakshi.__class__.role))
print("Sourav is also an {}".format(Sourav.__class__.role))

# Accessing instance attributes
print("My name is {}".format(Sakshi.name))
print("My name is {}".format(Sourav.name))
    