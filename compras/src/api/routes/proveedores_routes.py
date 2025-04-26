from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.adapters.proveedor_repository_sqlalchemy import ProveedorRepositorySQLAlchemy
from src.application.schemas.compras import ProveedorCreate, ProveedorRead
from src.config.database import SessionLocal

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])
repo = ProveedorRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProveedorRead)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    proveedor_existente = repo.obtener_por_nombre(db, proveedor.nombre)
    if proveedor_existente:
        raise HTTPException(status_code=400, detail="Ya existe un proveedor con ese nombre")
    return repo.guardar(db, proveedor)

@router.get("/", response_model=List[ProveedorRead])
def listar_proveedores(db: Session = Depends(get_db)):
    return repo.listar_todos(db)

@router.get("/{proveedor_id}", response_model=ProveedorRead)
def obtener_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = repo.obtener_por_id(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.delete("/{proveedor_id}")
def eliminar_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    proveedor = repo.eliminar(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return {"message": "Proveedor eliminado"}

@router.put("/{proveedor_id}", response_model=ProveedorRead)
def actualizar_proveedor(proveedor_id: int, proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    actualizado = repo.actualizar(db, proveedor_id, proveedor)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return actualizado