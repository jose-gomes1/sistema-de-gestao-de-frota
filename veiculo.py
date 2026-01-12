class Veiculo:
    def __init__(self, tipo, marca, modelo, preco, vel, combustivel, cor):
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo

        self.preco_base = preco   # preço SEM IVA (fixo)
        self.preco = preco        # preço exibido
        self.com_iva = False      # estado do IVA

        self.vel = vel
        self.combustivel = combustivel
        self.cor = cor

    def __str__(self):
        iva_txt = " (c/ IVA)" if self.com_iva else " (s/ IVA)"
        return (
            f"{self.tipo} | {self.marca} | {self.modelo} | "
            f"{self.preco:.2f}€{iva_txt} | {self.vel}km/h | "
            f"{self.combustivel} | {self.cor}"
        )
