from veiculo import Veiculo

class Mota(Veiculo):
    def __init__(self, marca, modelo, preco, vel, combustivel, cor):
        super().__init__("Mota", marca, modelo, preco, vel, combustivel, cor)

    def __repr__(self):
        return self.__str__()
