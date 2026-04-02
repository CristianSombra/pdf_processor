from sqlalchemy import text
from app.database.connection import engine

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Conexión a PostgreSQL exitosa.")
except Exception as error:
    print("Error de conexión:")
    print(error)