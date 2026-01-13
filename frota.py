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
                    if not linha:
                        continue  # 🔥 evita crash

                    tipo = linha[0]

                    if tipo == "Carro":
                        if len(linha) == 9:
                            _, marca, modelo, preco, vel, combustivel, cor, eletrico, consumo = linha
                            v = Carro(
                                marca, modelo, float(preco), int(vel),
                                combustivel, cor,
                                eletrico=eletrico == "True",
                                consumo_kwh=float(consumo)
                            )
                        elif len(linha) == 7:
                            _, marca, modelo, preco, vel, combustivel, cor = linha
                            v = Carro(marca, modelo, float(preco), int(vel), combustivel, cor)
                        else:
                            continue

                    elif tipo == "Mota":
                        if len(linha) == 8:
                            _, marca, modelo, preco, vel, combustivel, cor, cilindrada = linha
                            v = Mota(
                                marca, modelo, float(preco), int(vel),
                                combustivel, cor, int(cilindrada)
                            )
                        else:
                            continue
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
                if isinstance(v, Carro) and v.eletrico:
                    writer.writerow([
                        v.tipo, v.marca, v.modelo, v.preco_base,
                        v.vel, v.combustivel, v.cor,
                        v.eletrico, v.consumo_kwh
                    ])
                elif isinstance(v, Mota):
                    writer.writerow([
                        v.tipo, v.marca, v.modelo, v.preco_base,
                        v.vel, v.combustivel, v.cor,
                        v.cilindrada
                    ])
                else:
                    writer.writerow([
                        v.tipo, v.marca, v.modelo, v.preco_base,
                        v.vel, v.combustivel, v.cor
                    ])

    @log_operacao
    def desconto(self, carro, percentagem=0.1):
        for v in self.veiculos:
            if v is carro:
                if not v.com_iva:
                    v.preco = v.preco_base * (1 - percentagem)
                    v.com_iva = True
                else:
                    v.preco = v.preco_base
                    v.com_iva = False
                return v.preco

        print("Veículo não pertence à frota.")
        return None


    @log_operacao
    def filtrar_por_marca(self, marca):
        return [v for v in self.veiculos if v.marca == marca]