from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.adapters.orden_repository_sqlalchemy import OrdenCompraRepositorySQLAlchemy
from src.application.schemas.compras import OrdenCompraCreate, OrdenCompraRead
from src.config.database import SessionLocal

router = APIRouter(prefix="/ordenes", tags=["Órdenes de Compra"])
repo = OrdenCompraRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrdenCompraRead)
def crear_orden(orden: OrdenCompraCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, orden)

@router.get("/", response_model=List[OrdenCompraRead])
def listar_ordenes(db: Session = Depends(get_db)):
    return repo.listar_todas(db)

@router.get("/{orden_id}", response_model=OrdenCompraRead)
def obtener_orden(orden_id: int, db: Session = Depends(get_db)):
    orden = repo.obtener_por_id(db, orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden

@router.delete("/{orden_id}")
def eliminar_orden(orden_id: int, db: Session = Depends(get_db)):
    orden = repo.eliminar(db, orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"message": "Orden eliminada"}
