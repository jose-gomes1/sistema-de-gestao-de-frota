# Sistema de Gestão de Frota

Este projeto é um sistema simples de gestão de veículos e frotas, escrito em Python, com suporte para:

- Adicionar veículos à frota  
- Aplicar descontos aos veículos  
- Filtrar veículos por marca  
- Persistência de dados em ficheiro CSV  
- Logging de operações com timestamps  

---

## Estrutura do projeto

sistema-de-gestao-de-frota/
│
├── main.py # Ponto de entrada do programa
├── frota.py # Classe Frota e métodos relacionados
├── veiculo.py # Classe base Veículo
├── carro.py # Classe Carro (herda de Veículo)
├── decorators.py # Decorators (logging)
├── frota.csv # Ficheiro CSV com a frota (gerado automaticamente)
└── README.md # Este ficheiro


---

## Requisitos

- Python 3.8+
- Datetime 6.0

---


### Executar o programa

python3 main.py

O main.py contém exemplos de:
    Criação de frota
    Adição de veículos
    Aplicação de descontos
    Criação do ficheiro CSV
    Filtragem por marca e impressão de veículos

# Detalhes técnicos
    Carro herda de Veiculo e adiciona velocidade (vel) e tipo de combustível (combustivel)
    Frota mantém uma lista de veículos (self.veiculos)
    desconto() aplica diretamente o desconto sobre o preço do carro
    criarFicheiro() utiliza csv.writer para criar ou atualizar o ficheiro CSV
    filtrar_por_marca() retorna uma lista de veículos que correspondem à marca
    log_operacao é um decorator que imprime timestamp e operação executada