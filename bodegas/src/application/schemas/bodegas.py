from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

# ------------------------------
# Bodega
# ------------------------------

class BodegaBase(BaseModel):
    nombre: str
    ciudad: str
    pais: str
    direccion: str

class BodegaCreate(BodegaBase):
    pass

class BodegaRead(BodegaBase):
    id: int

    class Config:
        from_attributes = True

# ------------------------------
# Producto
# ------------------------------

class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    proveedor_id: Optional[int] = None
    precio_compra: Optional[float] = None
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
    cantidad_disponible: int
    class Config:
        from_attributes = True


# ------------------------------
# MovimientoInventario
# ------------------------------

class TipoMovimiento(str, Enum):
    entrada = "entrada"
    salida = "salida"
    traslado = "traslado"

class MovimientoInventarioBase(BaseModel):
    producto_id: UUID
    cantidad: int
    bodega_id: int
    tipo_movimiento: TipoMovimiento
    fecha: Optional[datetime] = None
    descripcion: Optional[str] = None

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventarioRead(MovimientoInventarioBase):
    id: int

    class Config:
        from_attributes = True

class ProductoUpdate(BaseModel):
    """
    Todos los campos opcionales: sólo envías los que quieres modificar.
    """
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    proveedor_id: Optional[int] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    promocion_activa: Optional[bool] = None
    fecha_vencimiento: Optional[datetime] = None
    condicion_almacenamiento: Optional[str] = None
    tiempo_entrega_dias: Optional[int] = None


# ------------------------------
# TrasladoInventario
# ------------------------------

class TrasladoInventarioCreate(BaseModel):
    producto_id: UUID
    origen_bodega_id: int
    destino_bodega_id: int
    cantidad: int = Field(..., gt=0, description="Debe ser mayor a cero")
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None

    @validator("destino_bodega_id")
    def origen_destino_distintos(cls, v, values):
        if "origen_bodega_id" in values and v == values["origen_bodega_id"]:
            raise ValueError("La bodega destino debe ser diferente a la bodega origen")
        return v

    class Config:
        from_attributes = True