import os
from openpyxl import Workbook
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QInputDialog,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
)
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from app.services.pdf_processor import procesar_pdf
from app.database.connection import SessionLocal
from app.database.models import Operacion


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
    "Socios - Dividendos",
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

        self.boton_ver_db = QPushButton("Ver base de datos")
        self.boton_ver_db.clicked.connect(self.ver_base_datos)
        botones_layout.addWidget(self.boton_ver_db)

        self.boton_exportar = QPushButton("Exportar")
        self.boton_exportar.clicked.connect(self.exportar_datos)
        botones_layout.addWidget(self.boton_exportar)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(11)
        self.tabla.setHorizontalHeaderLabels([
            "ID",
            "Operación Nro.",
            "Estado",
            "Fecha y Hora",
            "Titular",
            "CUIT",
            "Importe",
            "Concepto",
            "Observaciones",
            "Autorizante",
            "Categoría",
        ])
        self.tabla.setVisible(False)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setWordWrap(False)
        self.tabla.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.tabla.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        layout.addLayout(header_layout)
        layout.addWidget(self.label)
        layout.addLayout(botones_layout)
        layout.addWidget(self.log)
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    def limpiar_log(self):
        if self.procesando:
            QMessageBox.warning(self, "Procesamiento en curso", "No se puede limpiar mientras se están procesando archivos.")
            return

        self.tabla.setVisible(False)
        self.log.setVisible(True)
        self.log.clear()
        self.label.setText("Arrastrá uno o varios PDFs acá")

    def ver_base_datos(self):
        if self.procesando:
            QMessageBox.warning(self, "Procesamiento en curso", "Esperá a que termine el procesamiento actual.")
            return

        self.log.setVisible(False)
        self.tabla.setVisible(True)
        self.label.setText("Vista de base de datos")

        session = SessionLocal()

        try:
            operaciones = session.query(Operacion).order_by(Operacion.id.desc()).all()

            if not operaciones:
                self.tabla.setRowCount(0)
                QMessageBox.information(self, "Base de datos", "No hay datos en la base de datos.")
                return

            self.tabla.setRowCount(len(operaciones))

            for fila, op in enumerate(operaciones):
                self.tabla.setItem(fila, 0, QTableWidgetItem(str(op.id)))
                self.tabla.setItem(fila, 1, QTableWidgetItem(str(op.operacion_nro or "")))
                self.tabla.setItem(fila, 2, QTableWidgetItem(str(op.estado or "")))
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(op.fecha_hora or "")))
                self.tabla.setItem(fila, 4, QTableWidgetItem(str(op.titular_destino or "")))
                self.tabla.setItem(fila, 5, QTableWidgetItem(str(op.cuit or "")))
                self.tabla.setItem(fila, 6, QTableWidgetItem(str(op.importe_transferir or "")))
                self.tabla.setItem(fila, 7, QTableWidgetItem(str(op.concepto or "")))
                self.tabla.setItem(fila, 8, QTableWidgetItem(str(op.observaciones or "")))
                self.tabla.setItem(fila, 9, QTableWidgetItem(str(op.autorizante or "")))
                self.tabla.setItem(fila, 10, QTableWidgetItem(str(op.categoria or "")))

            self.tabla.resizeColumnsToContents()
            self.tabla.resizeRowsToContents()
            self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        except Exception as e:
            self.tabla.setVisible(False)
            self.log.setVisible(True)
            self.log.clear()
            self.log.append(f"Error al leer la base de datos: {e}")

        finally:
            session.close()

    def exportar_datos(self):
        if self.tabla.rowCount() == 0:
            QMessageBox.warning(self, "Exportar", "No hay datos para exportar.")
            return
    
        formato, ok = QInputDialog.getItem(
            self,
            "Exportar datos",
            "Seleccione el formato:",
            ["Excel", "PDF", "TXT"],
            0,
            False
        )
    
        if not ok or not formato:
            return
    
        if formato == "Excel":
            filtro = "Archivos Excel (*.xlsx)"
            extension = "xlsx"
        elif formato == "PDF":
            filtro = "Archivos PDF (*.pdf)"
            extension = "pdf"
        else:
            filtro = "Archivos de texto (*.txt)"
            extension = "txt"
    
        ruta_archivo, _ = QFileDialog.getSaveFileName(
            self,
            f"Guardar como {formato}",
            f"base_datos_exportada.{extension}",
            filtro
        )
    
        if not ruta_archivo:
            return
    
        try:
            if formato == "TXT":
                with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                    encabezados = []
                    for col in range(self.tabla.columnCount()):
                        encabezados.append(self.tabla.horizontalHeaderItem(col).text())
                    archivo.write(" | ".join(encabezados) + "\n")
                    archivo.write("-" * 200 + "\n")
    
                    for fila in range(self.tabla.rowCount()):
                        valores = []
                        for col in range(self.tabla.columnCount()):
                            item = self.tabla.item(fila, col)
                            valores.append(item.text() if item else "")
                        archivo.write(" | ".join(valores) + "\n")
    
                QMessageBox.information(
                    self,
                    "Exportar",
                    f"Archivo TXT exportado correctamente:\n{ruta_archivo}"
                )
    
            elif formato == "Excel":
                workbook = Workbook()
                hoja = workbook.active
                hoja.title = "Base de datos"
    
                encabezados = []
                for col in range(self.tabla.columnCount()):
                    encabezados.append(self.tabla.horizontalHeaderItem(col).text())
                hoja.append(encabezados)
    
                for fila in range(self.tabla.rowCount()):
                    valores = []
                    for col in range(self.tabla.columnCount()):
                        item = self.tabla.item(fila, col)
                        valor = item.text() if item else ""

                        if col == 6:  # columna Importe
                            try:
                                valor = float(valor)
                            except ValueError:
                                valor = 0.0

                        valores.append(valor)

                    hoja.append(valores)
    
                for columna in hoja.columns:
                    max_largo = 0
                    letra_columna = columna[0].column_letter
    
                    for celda in columna:
                        valor = str(celda.value) if celda.value is not None else ""
                        if len(valor) > max_largo:
                            max_largo = len(valor)
    
                    hoja.column_dimensions[letra_columna].width = max_largo + 2

                for fila in range(2, hoja.max_row + 1):
                    hoja[f"G{fila}"].number_format = '#,##0.00'
    
                workbook.save(ruta_archivo)
    
                QMessageBox.information(
                    self,
                    "Exportar",
                    f"Archivo Excel exportado correctamente:\n{ruta_archivo}"
                )
    
            elif formato == "PDF":
                doc = SimpleDocTemplate(
                    ruta_archivo,
                    pagesize=landscape(letter),
                    leftMargin=20,
                    rightMargin=20,
                    topMargin=20,
                    bottomMargin=20
                )
            
                datos = []
            
                encabezados = []
                for col in range(self.tabla.columnCount()):
                    encabezados.append(self.tabla.horizontalHeaderItem(col).text())
                datos.append(encabezados)
            
                for fila in range(self.tabla.rowCount()):
                    fila_datos = []
                    for col in range(self.tabla.columnCount()):
                        item = self.tabla.item(fila, col)
                        fila_datos.append(item.text() if item else "")
                    datos.append(fila_datos)
            
                anchos_columnas = [30, 55, 45, 70, 130, 70, 55, 55, 85, 120, 60]
            
                tabla = Table(datos, colWidths=anchos_columnas, repeatRows=1)
            
                estilo = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 7),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ])
            
                tabla.setStyle(estilo)
            
                elementos = [tabla]
                doc.build(elementos)
            
                QMessageBox.information(
                    self,
                    "Exportar",
                    f"Archivo PDF exportado correctamente:\n{ruta_archivo}"
                )
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo exportar el archivo:\n{e}")

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

        self.tabla.setVisible(False)
        self.log.setVisible(True)

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