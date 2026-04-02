from app.services.pdf_processor import procesar_pdf

ruta_pdf = "samples/ACEVEDO SOLEDAD SEPTIEMBRE 2022.pdf"

resultado = procesar_pdf(ruta_pdf, "Enfermería")

print(resultado["mensaje"])