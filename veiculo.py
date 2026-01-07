class Veiculo:
    def __init__(self, marca, preco):
        self.marca = marca
        self.preco = preco

    def __str__(self):
        return f"{self.marca} - {self.preco}€"