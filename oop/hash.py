import hashlib

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = self._hash_password(master_password)
        self.passwords = {}

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_password(self, service, password):
        self.passwords[service] = self._hash_password(password)

    def get_password(self, service, master_password):
        if self._hash_password(master_password) == self.master_password:
            return self.passwords.get(service, "Service not found")
        return "Access denied"

manager = PasswordManager("master123")
manager.add_password("email", "emailpass")
print(manager.get_password("email", "master123"))  # Hashed password