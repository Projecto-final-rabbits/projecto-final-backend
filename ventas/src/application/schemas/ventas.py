
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

# ------------------------------
# Producto
# ------------------------------
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_venta: float
    categoria: Optional[str] = None
    promocion_activa: Optional[bool] = False

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int

    class Config:
        from_attributes = True


# ------------------------------
# Cliente
# ------------------------------
class ClienteBase(BaseModel):
    nombre: str
    tipo_cliente: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteRead(ClienteBase):
    id: int

    class Config:
        from_attributes = True


# ------------------------------
# Vendedor
# ------------------------------
class VendedorBase(BaseModel):
    nombre: str
    zona: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None

class VendedorCreate(VendedorBase):
    pass

class VendedorRead(VendedorBase):
    id: int

    class Config:
        from_attributes = True


# ------------------------------
# Pedido  ←─ aquí va el cambio
# ------------------------------
class ProductoCantidad(BaseModel):
    producto_id: int  # usa int para mantener consistencia con PK de la tabla productos
    cantidad: int = Field(gt=0)

class PedidoCreate(BaseModel):
    cliente_id: int
    vendedor_id: int
    fecha_envio: date
    direccion_entrega: str
    productos: List[ProductoCantidad]

class PedidoRead(BaseModel):
    id: int
    cliente_id: int
    vendedor_id: int
    fecha_envio: date
    direccion_entrega: str
    estado: str

    class Config:
        from_attributes = True

# ------------------------------
# DetallePedido
# ------------------------------
class DetallePedidoBase(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoRead(DetallePedidoBase):
    id: int

    class Config:
        from_attributes = True


# ------------------------------
# PlanVenta
# ------------------------------
class PlanVentaBase(BaseModel):
    vendedor_id: int
    producto_id: int
    cuota: int
    periodo: str

class PlanVentaCreate(PlanVentaBase):
    pass

class PlanVentaRead(PlanVentaBase):
    id: int

    class Config:
        from_attributes = True