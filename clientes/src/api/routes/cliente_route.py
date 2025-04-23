from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.config.database import SessionLocal
from src.infrastructure.adapters.cliente_repository_sqlalchemy import ClienteRepositorySQLAlchemy
from src.application.schemas.clientes import ClienteCreate, ClienteRead


router = APIRouter(prefix="/clientes", tags=["Clientes"])
repo_cliente = ClienteRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClienteRead)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return repo_cliente.guardar(db, cliente)

@router.get("/", response_model=List[ClienteRead])
def listar_clientes(db: Session = Depends(get_db)):
    return repo_cliente.listar_todos(db)

@router.get("/{cliente_id}", response_model=ClienteRead)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = repo_cliente.obtener_por_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return repo_cliente.eliminar(db, cliente_id)
