from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.vendedor_repository_sqlalchemy import VendedorRepositorySQLAlchemy
from src.application.schemas.ventas import VendedorCreate, VendedorRead

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])
repo = VendedorRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=VendedorRead)
def crear_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, vendedor)

@router.get("/", response_model=List[VendedorRead])
def listar_vendedores(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{vendedor_id}", response_model=VendedorRead)
def obtener_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    vendedor = repo.obtener_por_id(db, vendedor_id)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor no encontrado")
    return vendedor

@router.delete("/{vendedor_id}")
def eliminar_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
    return repo.eliminar(db, vendedor_id)
