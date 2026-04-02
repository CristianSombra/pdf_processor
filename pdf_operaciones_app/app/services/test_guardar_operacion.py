from app.services.pdf_reader import extraer_texto_pdf
from app.services.data_extractor import extraer_datos
from app.services.operacion_service import guardar_operacion

ruta_pdf = "samples/ACEVEDO SOLEDAD SEPTIEMBRE 2022.pdf"

texto = extraer_texto_pdf(ruta_pdf)
datos = extraer_datos(texto)

resultado = guardar_operacion(datos, "Enfermería")

print(resultado["mensaje"])