from veiculo import Veiculo

class Mota(Veiculo):
    def __init__(self, marca, modelo, preco, vel, combustivel, cor, cilindrada):
        super().__init__("Mota", marca, modelo, preco, vel, combustivel, cor)
        self.cilindrada = cilindrada
