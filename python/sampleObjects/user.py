class UserObject:

    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f'User: {self.name} - {self.phone} - {self.email}'