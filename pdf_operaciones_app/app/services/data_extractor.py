import re
from datetime import datetime


def limpiar_espacios(texto):
    return re.sub(r"\s+", " ", texto).strip()


def buscar_primer_patron(texto, patrones, flags=0):
    for patron in patrones:
        coincidencia = re.search(patron, texto, flags)
        if coincidencia:
            return coincidencia
    return None


def extraer_operacion_nro(texto):
    patrones = [
        r"(\d+)\s*Operación Nro\.",
        r"Operación Nro\.\s*(\d+)",
    ]
    coincidencia = buscar_primer_patron(texto, patrones)

    if coincidencia:
        return coincidencia.group(1).strip()

    return None


def extraer_estado(texto):
    patrones = [
        r"Estado\s+Control Nro\.\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+)",
        r"Control Nro\.\s+[^\n\r]+\s+Estado\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+)",
        r"Estado\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+)",
    ]
    coincidencia = buscar_primer_patron(texto, patrones)

    if coincidencia:
        return coincidencia.group(1).strip()

    return None


def extraer_fecha_hora(texto):
    patron = r"Fecha y Hora\s+(\d{2}/\d{2}/\d{4}\s*-\s*\d{2}:\d{2})"
    coincidencia = re.search(patron, texto)

    if coincidencia:
        fecha_texto = coincidencia.group(1).strip()
        return datetime.strptime(fecha_texto, "%d/%m/%Y - %H:%M")

    return None


def extraer_titular_destino(texto):
    patrones = [
        r"CBU Destino\s+\d+\s+Titular\s+([A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s,./'\-]+?)\s+CUIT / CUIL / CDI",
        r"CBU\s+\d+\s+Titular\s+([A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s,./'\-]+?)\s+CUIT / CUIL / CDI",
    ]
    coincidencia = buscar_primer_patron(texto, patrones)

    if coincidencia:
        return limpiar_espacios(coincidencia.group(1))

    return None

def extraer_cuit(texto):
    patron = r"CUIT / CUIL / CDI\s+([\d\-]+)"
    coincidencia = re.search(patron, texto)

    if coincidencia:
        return coincidencia.group(1).strip()

    return None


def extraer_importe_transferir(texto):
    patron = r"Importe a Transferir\s+\$\s*([\d\.,]+)"
    coincidencia = re.search(patron, texto)

    if coincidencia:
        return coincidencia.group(1).strip()

    return None


def extraer_concepto(texto):
    patron = r"Concepto\s+(.+?)\s+Referencia"
    coincidencia = re.search(patron, texto, re.DOTALL)

    if coincidencia:
        return limpiar_espacios(coincidencia.group(1))

    return None


def extraer_observaciones(texto):
    patrones = [
        r"Observaciones\s+(.+?)\s+Usuarios Intervinientes",
        r"Observaciones\s+(.+)",
    ]

    coincidencia = buscar_primer_patron(texto, patrones, re.DOTALL)

    if coincidencia:
        return limpiar_espacios(coincidencia.group(1))

    # fallback → usar Referencia si no hay Observaciones
    patron_referencia = r"Referencia\s+(.+?)\s+Usuarios Intervinientes"
    coincidencia_ref = re.search(patron_referencia, texto, re.DOTALL)

    if coincidencia_ref:
        return limpiar_espacios(coincidencia_ref.group(1))

    return None


def extraer_autorizante(texto):
    patron = r"Usuarios Intervinientes\s+Ingresante\s+(.+?)\s+\d{2}/\d{2}/\d{4}\s*-\s*\d{2}:\d{2}\s+Autorizantes"
    coincidencia = re.search(patron, texto, re.DOTALL)

    if coincidencia:
        return limpiar_espacios(coincidencia.group(1))

    return None


def extraer_datos(texto):
    return {
        "operacion_nro": extraer_operacion_nro(texto),
        "estado": extraer_estado(texto),
        "fecha_hora": extraer_fecha_hora(texto),
        "titular_destino": extraer_titular_destino(texto),
        "cuit": extraer_cuit(texto),
        "importe_transferir": extraer_importe_transferir(texto),
        "concepto": extraer_concepto(texto),
        "observaciones": extraer_observaciones(texto),
        "autorizante": extraer_autorizante(texto),
    }