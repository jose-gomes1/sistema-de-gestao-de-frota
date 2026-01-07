from frota import Frota
from carro import Carro

def main():
    f = Frota()
    c1 = Carro("BMW", 50000, 240, "Gasolina")
    c2 = Carro("Audi", 24000, 230, "Gasóleo")


    f.adicionar_veiculo(c1)
    f.adicionar_veiculo(c2)
    print(f"Desconto {c1.marca}:", f.desconto(c1))
    print(f"Desconto {c2.marca}:", f.desconto(c2))

    f.criarFicheiro()

    for carro in f.filtrar_por_marca("BMW"):
        print(carro)

if __name__ == "__main__":
    main()