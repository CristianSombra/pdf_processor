from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class WelcomeScreen(QWidget):
    def __init__(self, on_start):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        self.titulo = QLabel("Procesador de Datos - CAMSA SRL")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.boton_iniciar = QPushButton("Iniciar")
        self.boton_iniciar.setFixedWidth(160)
        self.boton_iniciar.setFixedHeight(40)
        self.boton_iniciar.clicked.connect(on_start)

        layout.addWidget(self.titulo)
        layout.addWidget(self.boton_iniciar, alignment=Qt.AlignCenter)

        self.setLayout(layout)