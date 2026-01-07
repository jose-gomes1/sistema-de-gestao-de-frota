from decorators import log_operacao

class Frota:
    def __init__(self):
        self.veiculos = []

    @log_operacao
    def adicionar_veiculo(self, v):
        self.veiculos.append(v)

    @log_operacao
    def criarFicheiro(self):
        with open("carros.csv", "w", encoding="utf-8") as f:
            for v in self.veiculos:
                f.write(str(v) + "\n")

    @log_operacao
    def desconto(self, preco):
        return preco * 0.1

    # List Comprehension
    def filtrar_por_marca(self, marca):
        return [v for v in self.veiculos if v.marca == marca]