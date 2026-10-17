from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class PiezaCatalogo(Base):
    __tablename__ = "piezas_catalogo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    part_dw = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)
