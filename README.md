# Procesador de PDFs - CAMSA SRL

Aplicación de escritorio desarrollada en Python para procesar archivos PDF, extraer información relevante y generar una base de datos estructurada para su posterior uso administrativo.

## Descripción

Este sistema permite cargar uno o varios archivos PDF, procesar su contenido y transformar la información en un formato organizado (por ejemplo, Excel), facilitando el análisis y la integración con otros procesos internos.

Está diseñado como herramienta complementaria del sistema de generación de órdenes de pago.

## Funcionalidades

- Carga de múltiples archivos PDF (drag & drop)
- Procesamiento automático del contenido de los PDFs
- Extracción de datos relevantes desde documentos
- Visualización de archivos cargados
- Limpieza y actualización de lista de PDFs (Refrescar)
- Acceso a la base de datos generada
- Exportación de datos procesados
- Interfaz gráfica simple e intuitiva
- Logo institucional integrado

## Tecnologías utilizadas

- Python 3
- PyQt5 (interfaz gráfica)
- Librerías de procesamiento de PDF (según implementación: PyPDF, pdfplumber, etc.)
- Pandas (transformación y estructuración de datos)
- PyInstaller (generación de ejecutable)

## Estructura del proyecto
