# src/interfaces/http/pedidos_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.db.models.venta_model import Pedido as PedidoORM
from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from src.application.schemas.ventas import PedidoCreate, PedidoRead, ProductoCantidad
from src.application.services.clientes_service import cliente_existe
from src.application.services.crear_pedido_detalle_service import CrearPedidoConDetalleService
from src.application.services.bodega_service import producto_en_stock
from src.application.schemas.ruta import DireccionesPedido
from src.application.services.pedidos_service import obtener_direcciones_pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=PedidoRead,
    status_code=status.HTTP_201_CREATED
)
def crear_pedido(
    pedido_in: PedidoCreate,
    db: Session = Depends(get_db)
):
    # 1) Asegurarnos de que el cliente existe
    if not cliente_existe(pedido_in.cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # 2) Validar stock para cada producto solicitado
    for item in pedido_in.productos:
        # item.producto_id es UUID, item.cantidad es int
        if not producto_en_stock(item.producto_id, item.cantidad):
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para producto {item.producto_id}. "
                       f"Se solicitaron {item.cantidad} unidades."
            )

    # 3) Si todo pasó, creamos el pedido
    repo = PedidoRepositorySQLAlchemy(db)
    servicio = CrearPedidoConDetalleService(repo)
    return servicio.execute(pedido_in)


@router.get(
    "/",
    response_model=List[PedidoRead]
)
def listar_pedidos(db: Session = Depends(get_db)):
    pedidos_orm = (
        db.query(PedidoORM)
          .options(joinedload(PedidoORM.detalles))
          .all()
    )
    resultado: List[PedidoRead] = []
    for p in pedidos_orm:
        productos = [
            ProductoCantidad(producto_id=d.producto_id, cantidad=d.cantidad)
            for d in p.detalles
        ]
        total = sum(d.cantidad * d.precio_unitario for d in p.detalles)
        resultado.append(
            PedidoRead(
                id=p.id,
                cliente_id=p.cliente_id,
                vendedor_id=p.vendedor_id,
                fecha_envio=p.fecha_envio,
                direccion_entrega=p.direccion_entrega,
                origen_bodega_id=p.origen_bodega_id,
                estado=p.estado,
                productos=productos,
                total=total,
            )
        )
    return resultado


@router.get(
    "/{pedido_id}",
    response_model=PedidoRead
)
def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    pedido_orm = (
        db.query(PedidoORM)
          .options(joinedload(PedidoORM.detalles))
          .filter(PedidoORM.id == pedido_id)
          .first()
    )
    if not pedido_orm:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    productos = [
        ProductoCantidad(producto_id=d.producto_id, cantidad=d.cantidad)
        for d in pedido_orm.detalles
    ]
    total = sum(d.cantidad * d.precio_unitario for d in pedido_orm.detalles)
    return PedidoRead(
        id=pedido_orm.id,
        cliente_id=pedido_orm.cliente_id,
        vendedor_id=pedido_orm.vendedor_id,
        fecha_envio=pedido_orm.fecha_envio,
        direccion_entrega=pedido_orm.direccion_entrega,
        estado=pedido_orm.estado,
        productos=productos,
        total=total,
    )


@router.delete(
    "/{pedido_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    repo = PedidoRepositorySQLAlchemy(db)
    repo.eliminar(pedido_id)
    return

@router.get("/{pedido_id}/direcciones", response_model=DireccionesPedido)
def get_pedido_direcciones(pedido_id: int, db: Session = Depends(get_db)):
    return obtener_direcciones_pedido_service(pedido_id, db)