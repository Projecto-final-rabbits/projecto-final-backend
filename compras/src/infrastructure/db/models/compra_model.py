from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.config.database import Base

class Proveedor(Base):
    __tablename__ = 'proveedores'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais = Column(String)
    contacto = Column(String)
    telefono = Column(String)
    email = Column(String)

    productos = relationship("Producto", back_populates="proveedor")
    ordenes_compra = relationship("OrdenCompra", back_populates="proveedor")


class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio_compra = Column(Float)
    categoria = Column(String)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'))
    tiempo_entrega_dias = Column(Integer)

    proveedor = relationship("Proveedor", back_populates="productos")
    detalles = relationship("DetalleOrdenCompra", back_populates="producto")


class OrdenCompra(Base):
    __tablename__ = 'ordenes_compra'

    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'))
    fecha_orden = Column(Date)
    estado = Column(String)
    total = Column(Float)

    proveedor = relationship("Proveedor", back_populates="ordenes_compra")
    detalles = relationship("DetalleOrdenCompra", back_populates="orden")


class DetalleOrdenCompra(Base):
    __tablename__ = 'detalle_orden_compra'

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey('ordenes_compra.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)

    orden = relationship("OrdenCompra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")
