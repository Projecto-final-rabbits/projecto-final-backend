from sqlalchemy import Column, Integer, String
from src.config.database import Base

class CompraModel(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, index=True)
    producto = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    proveedor = Column(String, nullable=False)