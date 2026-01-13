from veiculo import Veiculo

class Mota(Veiculo):
    def __init__(self, marca, modelo, preco, vel, combustivel, cor, cilindrada):
        super().__init__("Mota", marca, modelo, preco, vel, combustivel, cor)
        self.cilindrada = cilindrada  # cc

    def __str__(self):
        base = super().__str__()
        return f"{base} | {self.cilindrada} cc"

    def __repr__(self):
        return self.__str__()
