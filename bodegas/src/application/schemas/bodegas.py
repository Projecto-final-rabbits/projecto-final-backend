from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

# ------------------------------
# Bodega
# ------------------------------

class BodegaBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    ciudad: str
    pais: str

class BodegaCreate(BodegaBase):
    pass

class BodegaRead(BodegaBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------
# Producto
# ------------------------------

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    proveedor_id: Optional[int] = None
    precio_compra: float
    precio_venta: float
    promocion_activa: Optional[bool] = False
    fecha_vencimiento: Optional[datetime] = None
    condicion_almacenamiento: Optional[str] = None
    tiempo_entrega_dias: Optional[int] = None

class ProductoCreate(ProductoBase):
    id: Optional[UUID] = None

class ProductoRead(ProductoBase):
    id: UUID

    class Config:
        orm_mode = True
        from_attributes = True


# ------------------------------
# Inventario
# ------------------------------

class InventarioBase(BaseModel):
    producto_id: UUID
    bodega_id: int
    cantidad_disponible: int

class InventarioCreate(InventarioBase):
    pass

class InventarioRead(InventarioBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------
# MovimientoInventario
# ------------------------------

class TipoMovimiento(str, Enum):
    entrada = "entrada"
    salida = "salida"

class MovimientoInventarioBase(BaseModel):
    producto_id: UUID
    cantidad: int
    tipo: TipoMovimiento
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventarioRead(MovimientoInventarioBase):
    id: int

    class Config:
        orm_mode = True
