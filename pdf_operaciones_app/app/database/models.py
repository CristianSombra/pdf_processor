from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Operacion(Base):
    __tablename__ = "operaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operacion_nro = Column(String(50), unique=True, nullable=False)
    estado = Column(String(100), nullable=True)
    fecha_hora = Column(DateTime, nullable=True)
    titular_destino = Column(String(255), nullable=True)
    cuit = Column(String(20), nullable=True)
    importe_transferir = Column(Numeric(15, 2), nullable=True)
    concepto = Column(String(255), nullable=True)
    observaciones = Column(Text, nullable=True)
    autorizante = Column(String(255), nullable=True)
    categoria = Column(String(100), nullable=False)