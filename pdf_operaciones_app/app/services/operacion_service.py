from decimal import Decimal
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
    "Otros"
]


def convertir_importe_a_decimal(importe_texto):
    if not importe_texto:
        return None

    importe_limpio = importe_texto.replace(".", "").replace(",", ".")
    return Decimal(importe_limpio)


def validar_datos_obligatorios(datos):
    campos_obligatorios = {
        "operacion_nro": "Operación Nro.",
        "estado": "Estado",
        "fecha_hora": "Fecha y hora",
        "titular_destino": "Titular destino",
        "cuit": "CUIT",
        "importe_transferir": "Importe a transferir",
    }

    for clave, nombre in campos_obligatorios.items():
        valor = datos.get(clave)

        if valor is None:
            return {
                "ok": False,
                "estado_proceso": "error",
                "mensaje": f"Falta el campo obligatorio: {nombre}"
            }

        if isinstance(valor, str) and not valor.strip():
            return {
                "ok": False,
                "estado_proceso": "error",
                "mensaje": f"Falta el campo obligatorio: {nombre}"
            }

    return {
        "ok": True,
        "estado_proceso": "valido",
        "mensaje": "Datos válidos."
    }


def guardar_operacion(datos, categoria):
    if categoria not in CATEGORIAS_VALIDAS:
        return {
            "ok": False,
            "estado_proceso": "error",
            "mensaje": f"Categoría inválida: {categoria}"
        }

    validacion = validar_datos_obligatorios(datos)

    if not validacion["ok"]:
        return validacion

    session = SessionLocal()

    try:
        operacion_existente = session.query(Operacion).filter_by(
            operacion_nro=datos["operacion_nro"]
        ).first()

        if operacion_existente:
            return {
                "ok": False,
                "estado_proceso": "duplicado",
                "mensaje": f"La operación {datos['operacion_nro']} ya existe en la base de datos."
            }

        nueva_operacion = Operacion(
            operacion_nro=datos["operacion_nro"],
            estado=datos["estado"],
            fecha_hora=datos["fecha_hora"],
            titular_destino=datos["titular_destino"],
            cuit=datos["cuit"],
            importe_transferir=convertir_importe_a_decimal(datos["importe_transferir"]),
            concepto=datos["concepto"],
            observaciones=datos["observaciones"],
            autorizante=datos["autorizante"],
            categoria=categoria,
        )

        session.add(nueva_operacion)
        session.commit()

        return {
            "ok": True,
            "estado_proceso": "guardado",
            "mensaje": f"La operación {datos['operacion_nro']} fue guardada correctamente."
        }

    except Exception as error:
        session.rollback()
        return {
            "ok": False,
            "estado_proceso": "error",
            "mensaje": f"Error al guardar la operación: {error}"
        }

    finally:
        session.close()