from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.db.models.venta_model import Pedido
from src.config.database import SessionLocal
from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from src.application.schemas.ventas import PedidoCreate, PedidoRead
from src.application.services.clientes_service import cliente_existe
from src.application.services.pedido_event_service import PedidoService
from src.infrastructure.adapters.out.pubsub_event_publisher import PubsubEventPublisher

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PedidoRead)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    if not cliente_existe(pedido.cliente_id):
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    repo = PedidoRepositorySQLAlchemy(db)
    creado = repo.guardar(pedido)

    event_publisher = PubsubEventPublisher()
    pedidos_service = PedidoService(event_publisher, repo)
    creado_schema = PedidoRead.from_orm(creado)

    try:
        pedidos_service.crear_pedido_event(creado_schema.dict())
    except Exception as e:
        print(f"⚠️ Error al publicar el evento de creación de pedido: {e}")

    return creado

@router.get("/", response_model=List[PedidoRead])
def listar_pedidos(db: Session = Depends(get_db)):
    repo = PedidoRepositorySQLAlchemy(db)
    return repo.listar_todos(db)

@router.get("/{pedido_id}", response_model=PedidoRead)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    repo = PedidoRepositorySQLAlchemy(db)
    pedido = repo.obtener_por_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    repo = PedidoRepositorySQLAlchemy(db)
    return repo.eliminar(db, pedido_id)
