import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QListWidget, QListWidgetItem, QMessageBox, QComboBox, QColorDialog
)
from PyQt6.QtGui import QColor
from frota import Frota
from carro import Carro
from mota import Mota

class FrotaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.frota = Frota()
        self.setWindowTitle("Gestão de Frota")
        self.setGeometry(200, 200, 500, 400)
        self.init_ui()
        self.carregar_lista()

    def init_ui(self):
        # Campos de entrada
        # Tipo de veículo
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Carro", "Mota"])
        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Marca")
        self.modelo_input = QLineEdit()
        self.modelo_input.setPlaceholderText("Modelo")
        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("Preço")
        self.vel_input = QLineEdit()
        self.vel_input.setPlaceholderText("Velocidade")
        self.comb_input = QLineEdit()
        self.comb_input.setPlaceholderText("Combustível")
        # Botões
        btn_add = QPushButton("Adicionar Veículo")
        btn_add.clicked.connect(self.adicionar)
        self.cor_btn = QPushButton("Escolher Cor")
        self.cor_btn.clicked.connect(self.escolher_cor)
        self.cor = "#FFFFFF"
        btn_desconto = QPushButton("Aplicar Desconto 10%")
        btn_desconto.clicked.connect(self.aplicar_desconto)
        btn_remover = QPushButton("Remover Veículo")
        btn_remover.clicked.connect(self.remover)
        # Lista
        self.lista = QListWidget()
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Novo veículo"))
        layout.addWidget(self.tipo_combo)
        layout.addWidget(self.marca_input)
        layout.addWidget(self.modelo_input) 
        layout.addWidget(self.preco_input)
        layout.addWidget(self.vel_input)
        layout.addWidget(self.comb_input)
        layout.addWidget(self.cor_btn)
        layout.addWidget(btn_add)
        layout.addWidget(btn_desconto)
        layout.addWidget(btn_remover)
        layout.addWidget(QLabel("Frota"))
        layout.addWidget(self.lista)
        self.setLayout(layout)

    def carregar_lista(self):
        self.lista.clear()
        for v in self.frota.veiculos:
            texto = f"{v.tipo} | {v.marca} | {v.preco:.2f}€ | {v.vel}km/h | {v.combustivel} | {v.cor}"
            item = QListWidgetItem(texto)
            item.setBackground(QColor(v.cor))
            self.lista.addItem(item)

    def adicionar(self):
        try:
            tipo = self.tipo_combo.currentText()
            marca = self.marca_input.text()
            modelo = self.modelo_input.text()
            preco = float(self.preco_input.text())
            vel = int(self.vel_input.text())
            combustivel = self.comb_input.text()
            if tipo == "Carro":
                v = Carro(marca, modelo, preco, vel, combustivel, self.cor)
            else:
                v = Mota(marca, modelo, preco, vel, combustivel, self.cor)
            self.frota.adicionar_veiculo(v)
            self.frota.criarFicheiro()
            self.carregar_lista()
            self.limpar_campos()
        except ValueError:
            QMessageBox.warning(self, "Erro", "Dados inválidos")

    def aplicar_desconto(self):
        item = self.lista.currentRow()
        if item < 0:
            QMessageBox.information(self, "Info", "Selecione um veículo")
            return
        carro = self.frota.veiculos[item]
        self.frota.desconto(carro, 0.1)
        self.frota.criarFicheiro()
        self.carregar_lista()

    def escolher_cor(self):
        cor = QColorDialog.getColor()
        if cor.isValid():
            self.cor = cor.name()
            self.cor_btn.setStyleSheet(
                f"background-color: {self.cor}; color: white;"
            )

    def remover(self):
        item = self.lista.currentRow()
        if item < 0:
            QMessageBox.information(self, "Info", "Selecione um veículo para remover")
            return
        carro = self.frota.veiculos[item]
        confirm = QMessageBox.question(
            self,
            "Confirmar",
            "Tem a certeza que deseja remover este veículo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.frota.remover_veiculo(carro)
            self.frota.criarFicheiro()
            self.carregar_lista()

    def limpar_campos(self):
        self.marca_input.clear()
        self.modelo_input.clear()
        self.preco_input.clear()
        self.vel_input.clear()
        self.comb_input.clear()
        self.cor = "#FFFFFF"
        self.cor_btn.setStyleSheet("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = FrotaGUI()
    janela.show()
    sys.exit(app.exec())