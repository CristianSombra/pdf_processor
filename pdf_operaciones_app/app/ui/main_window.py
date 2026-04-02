from PySide6.QtWidgets import QApplication, QWidget, QStackedLayout
from app.ui.welcome_screen import WelcomeScreen
from app.ui.processor_screen import ProcessorScreen


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Procesador de Datos")
        self.setMinimumSize(700, 500)

        self.stacked_layout = QStackedLayout()
        self.setLayout(self.stacked_layout)

        self.welcome_screen = WelcomeScreen(self.mostrar_procesador)
        self.processor_screen = ProcessorScreen()

        self.stacked_layout.addWidget(self.welcome_screen)
        self.stacked_layout.addWidget(self.processor_screen)

        self.stacked_layout.setCurrentWidget(self.welcome_screen)

    def mostrar_procesador(self):
        self.stacked_layout.setCurrentWidget(self.processor_screen)


def run_app():
    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    app.exec()