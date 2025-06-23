class User:
    def __init__(self, username, email, telefone, cpf, cep, bairro, senha, is_admin=False):
        self.username = username
        self.email = email
        self.telefone = telefone
        self.cpf = cpf
        self.cep = cep
        self.bairro = bairro
        self.senha = senha
        self.is_admin = is_admin

    def get_info(self):
        return (
            f"Usuário: {self.username}, Email: {self.email}, "
            f"Telefone: {self.telefone}, CPF: {self.cpf}, "
            f"CEP: {self.cep}, Bairro: {self.bairro}, "
            f"Admin: {self.is_admin}"
        )
