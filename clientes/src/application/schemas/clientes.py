from pydantic import BaseModel
from typing import List, Optional


# Schemas para ContactoCliente
class ContactoClienteBase(BaseModel):
    nombre_contacto: str
    telefono: str
    email: str

class ContactoClienteCreate(ContactoClienteBase):
    pass

class ContactoClienteRead(ContactoClienteBase):
    id: int
    cliente_id: int

    class Config:
        orm_mode = True


# Schemas para DireccionEntrega
class DireccionEntregaBase(BaseModel):
    direccion: str
    ciudad: str
    pais: str

class DireccionEntregaCreate(DireccionEntregaBase):
    pass

class DireccionEntregaRead(DireccionEntregaBase):
    id: int
    cliente_id: int

    class Config:
        orm_mode = True


# Schemas para Tienda
class TiendaBase(BaseModel):
    nombre_tienda: str
    direccion: str
    zona: str

class TiendaCreate(TiendaBase):
    pass

class TiendaRead(TiendaBase):
    id: int
    cliente_id: int

    class Config:
        orm_mode = True


# Schemas para Pedido
class PedidoBase(BaseModel):
    estado: str
    direccion_entrega_id: int

class PedidoCreate(PedidoBase):
    cliente_id: int

class PedidoRead(PedidoBase):
    id: int
    cliente_id: int

    class Config:
        orm_mode = True


# Schemas para Cliente
class ClienteBase(BaseModel):
    nombre: str
    tipo_cliente: str
    email: str
    telefono: str
    fecha_registro: str

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id: int
    contacto_clientes: List[ContactoClienteRead] = []
    direccion_entregas: List[DireccionEntregaRead] = []
    tiendas: List[TiendaRead] = []
    pedidos: List[PedidoRead] = []

    class Config:
        orm_mode = True
