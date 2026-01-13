import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QListWidget, QListWidgetItem, QMessageBox, QComboBox, QColorDialog, QCheckBox
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
        self.setGeometry(200, 200, 500, 450)
        self.init_ui()
        self.carregar_lista()

    def init_ui(self):
        # Campos de entrada
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Veiculo", "Carro", "Mota"])
        self.tipo_combo.currentTextChanged.connect(self.atualizar_campos_tipo)

        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Marca")

        self.modelo_input = QLineEdit()
        self.modelo_input.setPlaceholderText("Modelo")

        self.preco_input = QLineEdit()
        self.preco_input.setPlaceholderText("Preço")

        self.vel_input = QLineEdit()
        self.vel_input.setPlaceholderText("Velocidade")

        self.comb_input = QComboBox()
        self.comb_input.addItems(["Gasolina", "Gasóleo"])

        # Motas
        self.cilindrada_input = QLineEdit()
        self.cilindrada_input.setPlaceholderText("Cilindrada (cc)")
        self.cilindrada_input.hide()

        # Carros elétricos
        self.eletrico_check = QCheckBox("Elétrico")
        self.eletrico_check.stateChanged.connect(self.toggle_consumo)
        self.eletrico_check.hide()

        self.consumo_input = QLineEdit()
        self.consumo_input.setPlaceholderText("Consumo (kWh/100km)")
        self.consumo_input.hide()

        self.marca_filtro_input = QLineEdit()
        self.marca_filtro_input.setPlaceholderText("Filtrar por marca")

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

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.clicked.connect(self.filtrar_por_marca_gui)

        # Lista de veículos
        self.lista = QListWidget()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Novo veículo"))
        layout.addWidget(self.tipo_combo)
        layout.addWidget(self.marca_input)
        layout.addWidget(self.modelo_input)
        layout.addWidget(self.preco_input)
        layout.addWidget(self.vel_input)
        layout.addWidget(self.cilindrada_input)
        layout.addWidget(self.comb_input)
        layout.addWidget(self.eletrico_check)
        layout.addWidget(self.consumo_input)
        layout.addWidget(self.cor_btn)
        layout.addWidget(btn_add)
        layout.addWidget(btn_desconto)
        layout.addWidget(btn_remover)
        layout.addWidget(QLabel("Frota"))
        layout.addWidget(self.lista)
        layout.addWidget(self.marca_filtro_input)
        layout.addWidget(btn_filtrar)

        self.setLayout(layout)

    # Atualiza campos quando muda o tipo de veículo
    def atualizar_campos_tipo(self, tipo):
        if tipo == "Carro":
            self.eletrico_check.show()
            self.cilindrada_input.hide()
            self.cilindrada_input.clear()
        elif tipo == "Mota":
            self.eletrico_check.hide()
            self.consumo_input.hide()
            self.eletrico_check.setChecked(False)
            self.cilindrada_input.show()

    # Mostra/oculta campo de consumo se o carro for elétrico
    def toggle_consumo(self):
        if self.eletrico_check.isChecked():
            self.consumo_input.show()
            # Desativa combustivel e define para 'Elétrico'
            self.comb_input.clear()
            self.comb_input.addItem("Elétrico")
            self.comb_input.setCurrentIndex(0)
            self.comb_input.setEnabled(False)
        else:
            self.consumo_input.hide()
            self.consumo_input.clear()
            # Reativa combustivel normal
            self.comb_input.clear()
            self.comb_input.addItems(["Gasolina", "Gasóleo"])
            self.comb_input.setEnabled(True)

    def carregar_lista(self):
        self.lista.clear()
        for v in self.frota.veiculos:
            texto = f"{v.tipo} | {v.marca} | {v.preco:.2f}€ | {v.vel}km/h | {v.combustivel} | {v.cor}"

            if isinstance(v, Carro) and getattr(v, "eletrico", False):
                texto += f" | Elétrico | {v.consumo_kwh} kWh/100km"

            if isinstance(v, Mota):
                texto += f" | {v.cilindrada} cc"

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
            combustivel = self.comb_input.currentText()

            if tipo == "Carro":
                if self.eletrico_check.isChecked():
                    consumo = float(self.consumo_input.text())
                    v = Carro(
                        marca, modelo, preco, vel, combustivel, self.cor,
                        eletrico=True, consumo_kwh=consumo
                    )
                else:
                    v = Carro(marca, modelo, preco, vel, combustivel, self.cor)
            else:  # Mota
                cilindrada = int(self.cilindrada_input.text())
                v = Mota(marca, modelo, preco, vel, combustivel, self.cor, cilindrada)
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
            self.cor_btn.setStyleSheet(f"background-color: {self.cor}; color: white;")

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

    def filtrar_por_marca_gui(self):
        marca = self.marca_filtro_input.text().strip()
        if not marca:
            self.carregar_lista()
            return

        veiculos_filtrados = self.frota.filtrar_por_marca(marca)
        self.lista.clear()
        for v in veiculos_filtrados:
            texto = f"{v.tipo} | {v.marca} {v.modelo} | {v.preco:.2f}€ | {v.vel}km/h | {v.combustivel} | {v.cor}"
            if isinstance(v, Carro) and getattr(v, "eletrico", False):
                texto += f" | Elétrico | {v.consumo_kwh} kWh/100km"
            if isinstance(v, Mota):
                texto += f" | {v.cilindrada} cc"
            item = QListWidgetItem(texto)
            item.setBackground(QColor(v.cor))
            self.lista.addItem(item)

    def limpar_campos(self):
        self.marca_input.clear()
        self.modelo_input.clear()
        self.preco_input.clear()
        self.vel_input.clear()
        self.cor = "#FFFFFF"
        self.cor_btn.setStyleSheet("")
        self.eletrico_check.setChecked(False)
        self.consumo_input.clear()
        self.consumo_input.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = FrotaGUI()
    janela.show()
    sys.exit(app.exec())
