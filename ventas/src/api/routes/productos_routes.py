from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.config.database import SessionLocal
from src.infrastructure.adapters.producto_repository_sqlalchemy import ProductoRepositorySQLAlchemy
from src.application.schemas.ventas import ProductoCreate, ProductoRead

router = APIRouter(prefix="/productos", tags=["Productos"])
repo = ProductoRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductoRead)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    return repo.guardar(db, producto)

@router.get("/", response_model=List[ProductoRead])
def listar_productos(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = repo.obtener_por_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    return repo.eliminar(db, producto_id)
