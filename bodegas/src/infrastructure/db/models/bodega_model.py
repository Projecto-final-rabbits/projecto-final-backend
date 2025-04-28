import uuid
from fastapi import HTTPException
from sqlalchemy import Column, String, Integer, Float, Date, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.config.database import Base
import enum

class TipoMovimientoEnum(enum.Enum):
    entrada = "entrada"
    salida = "salida"

class Bodega(Base):
    __tablename__ = 'bodegas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ciudad = Column(String, nullable=False)
    pais = Column(String, nullable=False)

    inventarios = relationship("Inventario", back_populates="bodega")


class Producto(Base):
    __tablename__ = 'productos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text)
    categoria = Column(String)
    precio_compra = Column(Float)
    precio_venta = Column(Float)
    promocion_activa = Column(String)
    fecha_vencimiento = Column(Date)
    proveedor_id = Column(String)
    condicion_almacenamiento = Column(String)
    tiempo_entrega_dias = Column(Integer)
    stock = Column(Integer)

    inventarios = relationship("Inventario", back_populates="producto")
    movimientos = relationship("MovimientoInventario", back_populates="producto")


class Inventario(Base):
    __tablename__ = 'inventarios'

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(UUID(as_uuid=True), ForeignKey('productos.id'), nullable=False)
    bodega_id = Column(Integer, ForeignKey('bodegas.id'), nullable=False)
    cantidad_disponible = Column(Integer)

    producto = relationship("Producto", back_populates="inventarios")
    bodega = relationship("Bodega", back_populates="inventarios")


class MovimientoInventario(Base):
    __tablename__ = 'movimientos_inventario'

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(UUID(as_uuid=True), ForeignKey('productos.id'), nullable=False)
    bodega_id = Column(Integer, ForeignKey('bodegas.id'), nullable=False)
    tipo_movimiento = Column(Enum(TipoMovimientoEnum))
    cantidad = Column(Integer)
    fecha = Column(Date)
    descripcion = Column(Text)

    producto = relationship("Producto", back_populates="movimientos")
    bodega = relationship("Bodega")