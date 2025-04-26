from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import Cliente
from src.application.schemas.ventas import ClienteCreate

class ClienteRepositorySQLAlchemy:

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, data: ClienteCreate) -> Cliente:
        cliente = Cliente(**data.dict())
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def listar_todos(self):
        return self.db.query(Cliente).all()

    def obtener_por_id(self, cliente_id: int):
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def eliminar(self, cliente_id: int):
        cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        self.db.delete(cliente)
        self.db.commit()
        return {"message": "Cliente eliminado"}
