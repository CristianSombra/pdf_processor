from app.services.pdf_reader import extraer_texto_pdf
from app.services.data_extractor import extraer_datos

ruta_pdf = "samples/ACEVEDO SOLEDAD SEPTIEMBRE 2022.pdf"

texto = extraer_texto_pdf(ruta_pdf)
datos = extraer_datos(texto)

print("Operación Nro.:", datos["operacion_nro"])
print("Estado:", datos["estado"])
print("Fecha y hora:", datos["fecha_hora"])
print("Titular destino:", datos["titular_destino"])
print("CUIT:", datos["cuit"])
print("Importe a transferir:", datos["importe_transferir"])
print("Concepto:", datos["concepto"])
print("Observaciones:", datos["observaciones"])
print("Autorizante:", datos["autorizante"])