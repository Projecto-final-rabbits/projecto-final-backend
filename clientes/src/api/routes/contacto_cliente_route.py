from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.config.database import SessionLocal
from src.infrastructure.adapters.contacto_cliente_reposiroty_sqlalchemy import ContactoClienteRepositorySQLAlchemy
from src.application.schemas.clientes import ContactoClienteCreate, ContactoClienteRead

router = APIRouter(prefix="/contactos", tags=["Contactos de Cliente"])
repo_contacto_cliente = ContactoClienteRepositorySQLAlchemy()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ContactoClienteRead)
def crear_contacto(contacto: ContactoClienteCreate, db: Session = Depends(get_db)):
    return repo_contacto_cliente.guardar(db, contacto)

@router.get("/", response_model=List[ContactoClienteRead])
def listar_contactos(db: Session = Depends(get_db)):
    return repo_contacto_cliente.listar_todos(db)

@router.get("/{contacto_id}", response_model=ContactoClienteRead)
def obtener_contacto(contacto_id: int, db: Session = Depends(get_db)):
    contacto = repo_contacto_cliente.obtener_por_id(db, contacto_id)
    if not contacto:
        raise HTTPException(status_code=404, detail="Contacto no encontrado")
    return contacto

@router.delete("/{contacto_id}")
def eliminar_contacto(contacto_id: int, db: Session = Depends(get_db)):
    return repo_contacto_cliente.eliminar(db, contacto_id)
