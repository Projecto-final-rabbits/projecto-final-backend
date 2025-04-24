
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.application.schemas.bodegas import MovimientoInventarioCreate, TipoMovimiento
from src.infrastructure.adapters.inventario_repository_sqlalchemy import InventarioRepository
from src.infrastructure.adapters.movimiento_repository_sqlalchemy import MovimientoInventarioRepository
from src.infrastructure.db.models.bodega_model import Inventario, MovimientoInventario

def registrar_entrada_producto_service(movimiento_data: MovimientoInventarioCreate, db: Session):
    if movimiento_data.tipo_movimiento != TipoMovimiento.entrada:
        raise HTTPException(status_code=400, detail="Este servicio solo admite movimientos de tipo 'entrada'")

    if movimiento_data.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a cero")

    inventario_repo = InventarioRepository(db)
    movimiento_repo = MovimientoInventarioRepository(db)

    # Verificar si ya existe inventario
    inventario = inventario_repo.obtener_por_producto_y_bodega(
        producto_id=movimiento_data.producto_id,
        bodega_id=movimiento_data.bodega_id
    )

    if inventario:
        inventario.cantidad_disponible += movimiento_data.cantidad
        inventario_repo.actualizar(inventario)
    else:
        nuevo_inventario = Inventario(
            producto_id=movimiento_data.producto_id,
            bodega_id=movimiento_data.bodega_id,
            cantidad_disponible=movimiento_data.cantidad
        )
        inventario_repo.crear(nuevo_inventario)

    nuevo_movimiento = MovimientoInventario(
        producto_id=movimiento_data.producto_id,
        bodega_id=movimiento_data.bodega_id,
        cantidad=movimiento_data.cantidad,
        tipo_movimiento=TipoMovimiento.entrada,
        descripcion=movimiento_data.descripcion,
        fecha=movimiento_data.fecha or datetime.now()
    )

    return movimiento_repo.crear(nuevo_movimiento)
