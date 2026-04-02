import logging
import os


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "procesamiento_pdfs.log")


def configurar_logger():
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("pdf_operaciones")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger