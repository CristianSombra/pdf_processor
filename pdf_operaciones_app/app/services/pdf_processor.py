import os
import shutil
from app.services.pdf_reader import extraer_texto_pdf
from app.services.data_extractor import extraer_datos
from app.services.operacion_service import guardar_operacion
from app.utils.logger import configurar_logger


CARPETA_PROCESADOS_OK = "samples/procesados_ok"
CARPETA_DUPLICADOS = "samples/duplicados"

logger = configurar_logger()


def procesar_pdf(ruta_pdf, categoria):
    try:
        texto = extraer_texto_pdf(ruta_pdf)
        datos = extraer_datos(texto)
        resultado = guardar_operacion(datos, categoria)

        nombre_archivo = os.path.basename(ruta_pdf)
        operacion_nro = datos.get("operacion_nro", "SIN_OPERACION")

        if resultado["estado_proceso"] == "guardado":
            os.makedirs(CARPETA_PROCESADOS_OK, exist_ok=True)
            destino = os.path.join(CARPETA_PROCESADOS_OK, nombre_archivo)

            if os.path.abspath(ruta_pdf) != os.path.abspath(destino):
                shutil.move(ruta_pdf, destino)

        elif resultado["estado_proceso"] == "duplicado":
            os.makedirs(CARPETA_DUPLICADOS, exist_ok=True)
            destino = os.path.join(CARPETA_DUPLICADOS, nombre_archivo)

            if os.path.abspath(ruta_pdf) != os.path.abspath(destino):
                shutil.move(ruta_pdf, destino)

        logger.info(
            f"archivo='{nombre_archivo}' | categoria='{categoria}' | operacion='{operacion_nro}' | estado='{resultado['estado_proceso']}' | mensaje='{resultado['mensaje']}'"
        )

        return resultado

    except Exception as error:
        nombre_archivo = os.path.basename(ruta_pdf)

        logger.error(
            f"archivo='{nombre_archivo}' | categoria='{categoria}' | estado='error' | mensaje='Error al procesar el PDF: {error}'"
        )

        return {
            "ok": False,
            "estado_proceso": "error",
            "mensaje": f"Error al procesar el PDF: {error}"
        }