class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_info(self):
        return f"Usuário: {self.username}, Email: {self.email}"