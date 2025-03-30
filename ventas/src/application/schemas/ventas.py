
from datetime import date
from typing import Optional
from pydantic import BaseModel

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

# ------------------------------
# Pedido
# ------------------------------

class PedidoBase(BaseModel):
    cliente_id: int
    vendedor_id: int
    fecha: Optional[date] = None
    estado: Optional[str] = "pendiente"
    total: Optional[float] = 0.0

class PedidoCreate(PedidoBase):
    pass

class PedidoRead(PedidoBase):
    id: int

    class Config:
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True
