from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.detalle_repository_sqlalchemy import DetallePedidoRepositorySQLAlchemy
from src.application.schemas.ventas import DetallePedidoCreate, DetallePedidoRead

router = APIRouter(prefix="/detalles", tags=["Detalles de Pedido"])
repo = DetallePedidoRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DetallePedidoRead)
def crear_detalle(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, detalle)

@router.get("/", response_model=List[DetallePedidoRead])
def listar_detalles(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{detalle_id}", response_model=DetallePedidoRead)
def obtener_detalle(detalle_id: int, db: Session = Depends(get_db)):
    detalle = repo.obtener_por_id(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.delete("/{detalle_id}")
def eliminar_detalle(detalle_id: int, db: Session = Depends(get_db)):
    return repo.eliminar(db, detalle_id)
