# src/interfaces/http/pedidos_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from src.infrastructure.db.models.venta_model import Pedido
from src.application.schemas.ventas import PedidoCreate, PedidoRead
from src.application.services.clientes_service import cliente_existe
from src.application.services.direcciones_service import direccion_entrega_existe
from src.application.services.pedido_event_service import PedidoService
from src.infrastructure.adapters.out.pubsub_event_publisher import PubsubEventPublisher
from src.application.services.crear_pedido_detalle_service import CrearPedidoConDetalleService

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
    # Validaciones de negocio externas (cliente, dirección, etc.)
    if not cliente_existe(pedido_in.cliente_id):
        raise HTTPException(404, "Cliente no encontrado")

    repo = PedidoRepositorySQLAlchemy(db)
    publisher = PubsubEventPublisher()

    servicio = CrearPedidoConDetalleService(repo, publisher)
    return servicio.execute(pedido_in)


@router.get(
    "/",
    response_model=List[PedidoRead]
)
def listar_pedidos(db: Session = Depends(get_db)):
    repo = PedidoRepositorySQLAlchemy(db)
    return repo.listar_todos()


@router.get(
    "/{pedido_id}",
    response_model=PedidoRead
)
def obtener_pedido(
    pedido_id: int,
    db: Session = Depends(get_db)
):
    repo = PedidoRepositorySQLAlchemy(db)
    pedido = repo.obtener_por_id(pedido_id)
    if not pedido:
        raise HTTPException(404, "Pedido no encontrado")
    return pedido


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
