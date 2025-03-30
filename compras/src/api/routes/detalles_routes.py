from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.adapters.detalle_repository_sqlalchemy import DetalleOrdenCompraRepositorySQLAlchemy
from src.application.schemas.compras import DetalleOrdenCompraCreate, DetalleOrdenCompraRead
from src.config.database import SessionLocal

router = APIRouter(prefix="/detalles", tags=["Detalles de Orden"])
repo = DetalleOrdenCompraRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DetalleOrdenCompraRead)
def crear_detalle(detalle: DetalleOrdenCompraCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, detalle)

@router.get("/", response_model=List[DetalleOrdenCompraRead])
def listar_detalles(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{detalle_id}", response_model=DetalleOrdenCompraRead)
def obtener_detalle(detalle_id: int, db: Session = Depends(get_db)):
    detalle = repo.obtener_por_id(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.delete("/{detalle_id}")
def eliminar_detalle(detalle_id: int, db: Session = Depends(get_db)):
    detalle = repo.eliminar(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"message": "Detalle eliminado"}
