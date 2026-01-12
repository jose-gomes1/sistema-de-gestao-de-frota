from veiculo import Veiculo

class Carro(Veiculo):
    def __init__(
        self, marca, modelo, preco, vel, combustivel, cor,
        eletrico=False, consumo_kwh=None
    ):
        super().__init__("Carro", marca, modelo, preco, vel, combustivel, cor)

        self.eletrico = eletrico           # True / False
        self.consumo_kwh = consumo_kwh     # kWh / 100km (ex: 15.2)

    def __str__(self):
        base = super().__str__()
        if self.eletrico:
            return f"{base} | Elétrico | {self.consumo_kwh} kWh/100km"
        return base
