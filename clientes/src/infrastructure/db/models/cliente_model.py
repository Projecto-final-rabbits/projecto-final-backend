from sqlalchemy import Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    tipo_cliente = Column(String)
    email = Column(String)
    telefono = Column(String)
    fecha_registro = Column(String)

    contacto_clientes = relationship("ContactoCliente", back_populates="cliente", cascade="all, delete-orphan")
    direccion_entregas = relationship("DireccionEntrega", back_populates="cliente", cascade="all, delete-orphan")
    tiendas = relationship("Tienda", back_populates="cliente", cascade="all, delete-orphan")
    pedidos = relationship("Pedido", back_populates="cliente")


class ContactoCliente(Base):
    __tablename__ = 'contacto_cliente'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    nombre_contacto = Column(String)
    telefono = Column(String)
    email = Column(String)

    cliente = relationship("Cliente", back_populates="contacto_clientes")


class DireccionEntrega(Base):
    __tablename__ = 'direccion_entrega'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    direccion = Column(String)
    ciudad = Column(String)
    pais = Column(String)

    cliente = relationship("Cliente", back_populates="direccion_entregas")

class Tienda(Base):
    __tablename__ = 'tiendas'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    nombre_tienda = Column(String)
    direccion = Column(String)
    zona = Column(String)

    cliente = relationship("Cliente", back_populates="tiendas")


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    vendedor_id = Column(Integer, nullable=False)
    fecha_envio = Column(Date, nullable=False)
    direccion_entrega = Column(String, nullable=False)
    estado = Column(String, nullable=False, default="pendiente")
    cliente = relationship("Cliente", back_populates="pedidos")
