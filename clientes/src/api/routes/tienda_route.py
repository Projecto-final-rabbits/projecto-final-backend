from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.config.database import SessionLocal
from src.infrastructure.adapters.tienda_repository_sqlalchemy import TiendaRepositorySQLAlchemy
from src.application.schemas.clientes import TiendaCreate, TiendaRead

router = APIRouter(prefix="/tiendas", tags=["Tiendas"])
repo_tienda = TiendaRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TiendaRead)
def crear_tienda(tienda: TiendaCreate, db: Session = Depends(get_db)):
    return repo_tienda.guardar(db, tienda)

@router.get("/", response_model=List[TiendaRead])
def listar_tiendas(db: Session = Depends(get_db)):
    return repo_tienda.listar_todos(db)

@router.get("/{tienda_id}", response_model=TiendaRead)
def obtener_tienda(tienda_id: int, db: Session = Depends(get_db)):
    tienda = repo_tienda.obtener_por_id(db, tienda_id)
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada")
    return tienda

@router.delete("/{tienda_id}")
def eliminar_tienda(tienda_id: int, db: Session = Depends(get_db)):
    return repo_tienda.eliminar(db, tienda_id)
