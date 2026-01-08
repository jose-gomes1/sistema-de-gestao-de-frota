class Veiculo:
    def __init__(self, tipo, marca, modelo, preco, vel, combustivel, cor):
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.preco = preco
        self.vel = vel
        self.combustivel = combustivel
        self.cor = cor

    def __str__(self):
        return f"{self.tipo} | {self.marca} | {self.modelo} | {self.preco:.2f}€ | {self.vel}km/h | {self.combustivel} | {self.cor}"