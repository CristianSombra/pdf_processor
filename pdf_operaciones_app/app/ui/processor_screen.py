from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QInputDialog,
    QMessageBox,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from app.services.pdf_processor import procesar_pdf


CATEGORIAS_VALIDAS = [
    "Oficina",
    "Cuidador",
    "Enfermería",
    "Médico",
    "Nutrición",
    "Kinesiología",
    "Fonoaudiología",
    "Terapista ocupacional",
    "Operador terapéutico",
    "Otros",
]


class ProcessorScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.procesando = False

        layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        self.logo_label = QLabel()
        pixmap = QPixmap("app/assets/logo_camsa.png")
        if not pixmap.isNull():
            self.logo_label.setPixmap(
                pixmap.scaled(
                    180,
                    70,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        self.logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()

        self.label = QLabel("Arrastrá uno o varios PDFs acá")
        self.label.setAlignment(Qt.AlignCenter)

        botones_layout = QHBoxLayout()
        botones_layout.addStretch()

        self.boton_limpiar = QPushButton("Refrescar")
        self.boton_limpiar.clicked.connect(self.limpiar_log)

        botones_layout.addWidget(self.boton_limpiar)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addLayout(header_layout)
        layout.addWidget(self.label)
        layout.addLayout(botones_layout)
        layout.addWidget(self.log)

        self.setLayout(layout)

    def limpiar_log(self):
        if self.procesando:
            QMessageBox.warning(self, "Procesamiento en curso", "No se puede limpiar mientras se están procesando archivos.")
            return

        self.log.clear()
        self.label.setText("Arrastrá uno o varios PDFs acá")

    def dragEnterEvent(self, event):
        if self.procesando:
            event.ignore()
            return

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.procesando:
            QMessageBox.warning(self, "Procesamiento en curso", "Esperá a que termine el procesamiento actual.")
            return

        archivos = event.mimeData().urls()

        rutas_pdf = []
        for archivo in archivos:
            ruta = archivo.toLocalFile()
            if ruta.lower().endswith(".pdf"):
                rutas_pdf.append(ruta)

        if not rutas_pdf:
            QMessageBox.warning(self, "Aviso", "No se soltaron archivos PDF válidos.")
            return

        categoria, ok = QInputDialog.getItem(
            self,
            "Seleccione el tipo de grupo",
            "Categoría:",
            CATEGORIAS_VALIDAS,
            0,
            False
        )

        if not ok or not categoria:
            self.log.append("❌ Procesamiento cancelado: no se seleccionó categoría.")
            return

        resumen = {
            "total": 0,
            "guardados": 0,
            "duplicados": 0,
            "errores": 0,
        }

        self.procesando = True
        self.label.setText(f"Procesando PDFs... Categoría seleccionada: {categoria}")

        try:
            for ruta in rutas_pdf:
                resultado = procesar_pdf(ruta, categoria)

                mensaje = resultado["mensaje"]
                estado = resultado["estado_proceso"]

                resumen["total"] += 1

                if estado == "guardado":
                    resumen["guardados"] += 1
                    linea = f"✔ [{categoria}] {ruta} → {mensaje}"
                elif estado == "duplicado":
                    resumen["duplicados"] += 1
                    linea = f"⚠ [{categoria}] {ruta} → {mensaje}"
                else:
                    resumen["errores"] += 1
                    linea = f"❌ [{categoria}] {ruta}\n    ERROR: {mensaje}"

                self.log.append(linea)

            self.log.append("")
            self.log.append("===== RESUMEN =====")
            self.log.append(f"Categoría: {categoria}")
            self.log.append(f"Total: {resumen['total']}")
            self.log.append(f"Guardados: {resumen['guardados']}")
            self.log.append(f"Duplicados: {resumen['duplicados']}")
            self.log.append(f"Errores: {resumen['errores']}")
            self.log.append("")

        finally:
            self.procesando = False
            self.label.setText("Arrastrá uno o varios PDFs acá")