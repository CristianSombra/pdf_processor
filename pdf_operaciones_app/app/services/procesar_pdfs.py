import os
from app.services.pdf_processor import procesar_pdf


CARPETA_PDFS = "samples"


def procesar_pdfs(categoria):
    archivos = os.listdir(CARPETA_PDFS)

    for archivo in archivos:
        ruta_pdf = os.path.join(CARPETA_PDFS, archivo)

        if os.path.isfile(ruta_pdf) and archivo.lower().endswith(".pdf"):
            resultado = procesar_pdf(ruta_pdf, categoria)
            print(f"{archivo} -> {resultado['mensaje']}")


if __name__ == "__main__":
    procesar_pdfs("Otros")