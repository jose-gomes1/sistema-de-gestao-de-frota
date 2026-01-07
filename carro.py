from veiculo import Veiculo

class Carro(Veiculo):
    def __init__(self, marca, preco, vel, combustivel):
        super().__init__(marca, preco)
        self.vel = vel
        self.combustivel = combustivel

    def __str__(self):
        return f"{self.marca} | {self.preco}€ | {self.vel} km/h | {self.combustivel}"

    def __repr__(self):
        return self.__str__()