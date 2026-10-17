from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class VehiculoCatalogo(Base):
    __tablename__ = "vehiculos_catalogo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(80), nullable=False)
    anio_desde = Column(Integer, nullable=True)
    anio_hasta = Column(Integer, nullable=True)
    tipo = Column(String(30), nullable=True)
    popularidad = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
