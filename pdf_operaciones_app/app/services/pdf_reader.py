import fitz

def extraer_texto_pdf(ruta_pdf):
    texto_completo = ""

    with fitz.open(ruta_pdf) as pdf:
        for pagina in pdf:
            texto_completo += pagina.get_text()

    return texto_completo