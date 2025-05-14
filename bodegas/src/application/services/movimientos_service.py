
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.application.schemas.bodegas import MovimientoInventarioCreate, TipoMovimiento, TrasladoInventarioCreate
from src.infrastructure.adapters.inventario_repository_sqlalchemy import InventarioRepository
from src.infrastructure.adapters.movimiento_repository_sqlalchemy import MovimientoInventarioRepository
from src.infrastructure.db.models.bodega_model import Inventario, MovimientoInventario, Bodega, Producto

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

def registrar_salida_producto_service(movimiento_data: MovimientoInventarioCreate, db: Session):
    if movimiento_data.tipo_movimiento != TipoMovimiento.salida:
        raise HTTPException(status_code=400, detail="Este servicio solo admite movimientos de tipo 'salida'")

    if movimiento_data.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor a cero")

    inventario_repo = InventarioRepository(db)
    movimiento_repo = MovimientoInventarioRepository(db)

    inventario = inventario_repo.obtener_por_producto_y_bodega(
        producto_id=movimiento_data.producto_id,
        bodega_id=movimiento_data.bodega_id
    )

    if not inventario:
        raise HTTPException(status_code=404, detail="No se encontró el inventario para el producto")

    if inventario.cantidad_disponible < movimiento_data.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    inventario.cantidad_disponible -= movimiento_data.cantidad
    inventario_repo.actualizar(inventario)

    nuevo_movimiento = MovimientoInventario(
        producto_id=movimiento_data.producto_id,
        bodega_id=movimiento_data.bodega_id,
        cantidad=movimiento_data.cantidad,
        tipo_movimiento=TipoMovimiento.salida,
        descripcion=movimiento_data.descripcion,
        fecha=movimiento_data.fecha or datetime.now()
    )

    return movimiento_repo.crear(nuevo_movimiento)

def registrar_traslado_producto_service(traslado_data: TrasladoInventarioCreate, db: Session
):
    # 1. Validar bodegas
    if not db.query(Bodega).get(traslado_data.origen_bodega_id):
        raise HTTPException(404, "Bodega origen no encontrada")
    if not db.query(Bodega).get(traslado_data.destino_bodega_id):
        raise HTTPException(404, "Bodega destino no encontrada")

    # 2. Validar producto
    if not db.query(Producto).get(traslado_data.producto_id):
        raise HTTPException(404, "Producto no encontrado")

    inv_repo = InventarioRepository(db)
    mov_repo = MovimientoInventarioRepository(db)

    # 3. Inventario origen y stock disponible
    inv_origen = inv_repo.obtener_por_producto_y_bodega(
        traslado_data.producto_id, traslado_data.origen_bodega_id
    )
    if not inv_origen:
        raise HTTPException(404, "No hay inventario en bodega origen")
    if inv_origen.cantidad_disponible < traslado_data.cantidad:
        raise HTTPException(400, "Stock insuficiente en bodega origen")

    # 4. Restar del inventario origen
    inv_origen.cantidad_disponible -= traslado_data.cantidad
    inv_repo.actualizar(inv_origen)

    # 5. Sumar (o crear) inventario destino
    inv_destino = inv_repo.obtener_por_producto_y_bodega(
        traslado_data.producto_id, traslado_data.destino_bodega_id
    )
    if inv_destino:
        inv_destino.cantidad_disponible += traslado_data.cantidad
        inv_repo.actualizar(inv_destino)
    else:
        inv_destino = Inventario(
            producto_id=traslado_data.producto_id,
            bodega_id=traslado_data.destino_bodega_id,
            cantidad_disponible=traslado_data.cantidad,
        )
        inv_repo.crear(inv_destino)

    # 6. Crear movimiento de traslado (se asocia a la bodega origen)
    nuevo_mov = MovimientoInventario(
        producto_id=traslado_data.producto_id,
        bodega_id=traslado_data.origen_bodega_id,
        cantidad=traslado_data.cantidad,
        tipo_movimiento=TipoMovimiento.traslado,
        descripcion=traslado_data.descripcion,
        fecha=traslado_data.fecha or datetime.now(),
    )
    return mov_repo.crear(nuevo_mov)