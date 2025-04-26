from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from src.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    precio_venta = Column(Float)
    categoria = Column(String)
    promocion_activa = Column(Boolean, default=False)

    detalles = relationship("DetallePedido", back_populates="producto")
    planes_venta = relationship("PlanVenta", back_populates="producto")


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo_cliente = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)

    pedidos = relationship("Pedido", back_populates="cliente")


class Vendedor(Base):
    __tablename__ = 'vendedores'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    zona = Column(String)
    email = Column(String)
    telefono = Column(String)

    pedidos = relationship("Pedido", back_populates="vendedor")
    planes_venta = relationship("PlanVenta", back_populates="vendedor")


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    vendedor_id = Column(Integer, ForeignKey('vendedores.id'))
    fecha = Column(Date)
    estado = Column(String)
    total = Column(Float)

    cliente = relationship("Cliente", back_populates="pedidos")
    vendedor = relationship("Vendedor", back_populates="pedidos")
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")


class DetallePedido(Base):
    __tablename__ = 'detalle_pedido'

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    producto_id = Column(UUID(as_uuid=True), ForeignKey('productos.id'))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles")


class PlanVenta(Base):
    __tablename__ = 'planes_venta'

    id = Column(Integer, primary_key=True, index=True)
    vendedor_id = Column(Integer, ForeignKey('vendedores.id'))
    producto_id = Column(UUID(as_uuid=True), ForeignKey('productos.id'))
    cuota = Column(Integer)
    periodo = Column(String)

    vendedor = relationship("Vendedor", back_populates="planes_venta")
    producto = relationship("Producto", back_populates="planes_venta")
