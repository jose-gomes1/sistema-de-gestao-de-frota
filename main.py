from frota import Frota
from carro import Carro

def main():
    f = Frota()
    c1 = Carro("BMW", 30000, 240, "Gasolina")
    c2 = Carro("Audi", 28000, 230, "Diesel")


    f.adicionar_veiculo(c1)
    f.adicionar_veiculo(c2)
    print(f"Desconto {c1.marca}:", f.desconto(c1.preco))
    print(f"Desconto {c2.marca}:", f.desconto(c2.preco))

    print(f.filtrar_por_marca("BMW"))
    f.criarFicheiro()

if __name__ == "__main__":
    main()