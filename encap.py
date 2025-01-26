class Public:
    def __init__(self):
        self.name = "John"  # Public attribute

    def display_name(self):
        print(self.name)  # Public method

obj = Public()
obj.display_name()  # Accessible
print(obj.name)  # Accessible


class Protected:
    def __init__(self):
        self._age = 30  # Protected attribute   ;    kanzidou _9bel mn l attribute

class Subclass(Protected): #héritage hna
    def display_age(self):
        print(self._age)  # Accessible in subclass   ; 
        #safi 7dha hna & if i want to instanciate an obj from the protected class maghadich tkhdeeem

obj = Subclass()
obj.display_age()

#obj = Protected()
#obj.display_age()



class Private:
    def __init__(self):
        self.__salary = 50000  # Private attribute    with __

    def salary(self):
        return self.__salary  # Access through public method

obj = Private()
print(obj.salary())  # Works
#print(obj.__salary)  # Raises AttributeError

