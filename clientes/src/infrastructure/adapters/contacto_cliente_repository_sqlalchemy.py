from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.cliente_model import ContactoCliente
from src.application.schemas.clientes import ContactoClienteCreate

class ContactoClienteRepositorySQLAlchemy:
    def guardar(self, db: Session, data: ContactoClienteCreate) -> ContactoCliente:
        contacto = ContactoCliente(**data.dict())
        db.add(contacto)
        db.commit()
        db.refresh(contacto)
        return contacto

    def listar_todos(self, db: Session):
        return db.query(ContactoCliente).all()

    def obtener_por_id(self, db: Session, contacto_id: int):
        return db.query(ContactoCliente).filter(ContactoCliente.id == contacto_id).first()

    def eliminar(self, db: Session, contacto_id: int):
        contacto = db.query(ContactoCliente).filter(ContactoCliente.id == contacto_id).first()
        if not contacto:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        db.delete(contacto)
        db.commit()
        return {"message": "Contacto eliminado"}
