class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, input_password):
        return self.password == input_password

user1 = User("admin", "secure123")
print(user1.authenticate("wrongpass"))


class Admin(User):
    def __init__(self, username, password, permissions):
        super().__init__(username, password)
        self.permissions = permissions

admin = Admin("superadmin", "admin123", ["read", "write", "delete"])
print(admin.authenticate("admin123"))


class Guest(User):
    def authenticate(self, input_password):
        return False  # Guests cannot authenticate

users = [User("user1", "pass1"), Admin("admin1", "adminpass", []), Guest("guest", "")]
for user in users:
    print(user.authenticate("pass1"))
    
    
    
class SecureUser:
    def __init__(self, username, password):
        self.username = username
        self.__password = password  # Private attribute

    def get_password(self):
        return "Access denied"  # Hide the actual password

user = SecureUser("user", "mypass")
print(user.get_password())  # Access denied


from abc import ABC, abstractmethod

class Authenticator(ABC):
    @abstractmethod
    def authenticate(self, input_password):
        pass

class PasswordAuthenticator(Authenticator):
    def authenticate(self, input_password):
        return input_password == "secret"

auth = PasswordAuthenticator()
print(auth.authenticate("secret"))  # True