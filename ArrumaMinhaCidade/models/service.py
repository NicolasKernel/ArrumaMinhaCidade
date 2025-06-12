class Service:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def get_details(self):
        return f"Serviço: {self.name}, Categoria: {self.category}"