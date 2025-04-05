from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.config.database import SessionLocal
from src.infrastructure.adapters.direccion_entrega_repository_sqlalchemy import DireccionEntregaRepositorySQLAlchemy
from src.application.schemas.clientes import DireccionEntregaCreate, DireccionEntregaRead

router = APIRouter(prefix="/direcciones", tags=["Direcciones de Entrega"])
repo_direccion_entrega = DireccionEntregaRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DireccionEntregaRead)
def crear_direccion(direccion: DireccionEntregaCreate, db: Session = Depends(get_db)):
    return repo_direccion_entrega.guardar(db, direccion)

@router.get("/", response_model=List[DireccionEntregaRead])
def listar_direcciones(db: Session = Depends(get_db)):
    return repo_direccion_entrega.listar_todos(db)

@router.get("/{direccion_id}", response_model=DireccionEntregaRead)
def obtener_direccion(direccion_id: int, db: Session = Depends(get_db)):
    direccion = repo_direccion_entrega.obtener_por_id(db, direccion_id)
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return direccion

@router.delete("/{direccion_id}")
def eliminar_direccion(direccion_id: int, db: Session = Depends(get_db)):
    return repo_direccion_entrega.eliminar(db, direccion_id)
