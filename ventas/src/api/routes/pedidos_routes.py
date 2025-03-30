from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from src.application.schemas.ventas import PedidoCreate, PedidoRead

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])
repo = PedidoRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PedidoRead)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, pedido)

@router.get("/", response_model=List[PedidoRead])
def listar_pedidos(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{pedido_id}", response_model=PedidoRead)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = repo.obtener_por_id(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return repo.eliminar(db, pedido_id)
