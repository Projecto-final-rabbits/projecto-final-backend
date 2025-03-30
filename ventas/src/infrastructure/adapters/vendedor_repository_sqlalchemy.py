from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import Vendedor
from src.application.schemas.ventas import VendedorCreate

class VendedorRepositorySQLAlchemy:
    def guardar(self, db: Session, data: VendedorCreate) -> Vendedor:
        vendedor = Vendedor(**data.dict())
        db.add(vendedor)
        db.commit()
        db.refresh(vendedor)
        return vendedor

    def listar_todos(self, db: Session):
        return db.query(Vendedor).all()

    def obtener_por_id(self, db: Session, vendedor_id: int):
        return db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()

    def eliminar(self, db: Session, vendedor_id: int):
        vendedor = db.query(Vendedor).filter(Vendedor.id == vendedor_id).first()
        if not vendedor:
            raise HTTPException(status_code=404, detail="Vendedor no encontrado")
        db.delete(vendedor)
        db.commit()
        return {"message": "Vendedor eliminado"}
