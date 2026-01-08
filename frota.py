import csv
from carro import Carro
from mota import Mota
from decorators import log_operacao

class Frota:
    def __init__(self):
        self.veiculos = []
        self.load("frota.csv")

    @log_operacao
    def load(self, file):
        try:
            with open(file, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for linha in reader:
                    if len(linha) == 7:  # <--- aqui deve ser 7
                        tipo, marca, modelo, preco, vel, combustivel, cor = linha

                        if tipo == "Carro":
                            v = Carro(marca, modelo, float(preco), int(vel), combustivel, cor)
                        elif tipo == "Mota":
                            v = Mota(marca, modelo, float(preco), int(vel), combustivel, cor)
                        else:
                            continue

                        self.veiculos.append(v)
        except FileNotFoundError:
            pass


    @log_operacao
    def adicionar_veiculo(self, v):
        self.veiculos.append(v)

    @log_operacao
    def remover_veiculo(self, carro):
        if carro in self.veiculos:
            self.veiculos.remove(carro)
            return True
        return False

    @log_operacao
    def criarFicheiro(self, nome_ficheiro="frota.csv"):
        with open(nome_ficheiro, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for v in self.veiculos:
                writer.writerow([
                    v.tipo, v.marca, v.modelo ,v.preco, v.vel, v.combustivel, v.cor
                ])

    @log_operacao
    def desconto(self, carro, percentagem=0.1):
        for v in self.veiculos:
            if v.marca == carro.marca and v.preco == carro.preco:
                v.preco *= (1 - percentagem)
                return v.preco
        print("Carro não pertence à frota.")
        return None

    @log_operacao
    def filtrar_por_marca(self, marca):
        return [v for v in self.veiculos if v.marca == marca]