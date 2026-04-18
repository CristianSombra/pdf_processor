import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Detectar si está en ejecutable
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / "config" / ".env"

load_dotenv(ENV_PATH)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")