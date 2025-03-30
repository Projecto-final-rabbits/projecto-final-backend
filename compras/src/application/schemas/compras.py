from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# ------------------------------
# Proveedor
# ------------------------------

class ProveedorBase(BaseModel):
    nombre: str
    pais: Optional[str] = None
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorRead(ProveedorBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------
# Producto
# ------------------------------

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_compra: float
    categoria: Optional[str] = None
    proveedor_id: int
    tiempo_entrega_dias: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------
# OrdenCompra
# ------------------------------

class OrdenCompraBase(BaseModel):
    proveedor_id: int
    fecha_orden: Optional[date] = None
    estado: Optional[str] = "pendiente"
    total: Optional[float] = 0.0

class OrdenCompraCreate(OrdenCompraBase):
    pass

class OrdenCompraRead(OrdenCompraBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------
# DetalleOrdenCompra
# ------------------------------

class DetalleOrdenCompraBase(BaseModel):
    orden_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetalleOrdenCompraCreate(DetalleOrdenCompraBase):
    pass

class DetalleOrdenCompraRead(DetalleOrdenCompraBase):
    id: int

    class Config:
        orm_mode = True
