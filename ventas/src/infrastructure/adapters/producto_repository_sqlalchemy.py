from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import Producto
from src.application.schemas.ventas import ProductoCreate

class ProductoRepositorySQLAlchemy:
    def guardar(self, db: Session, data: ProductoCreate) -> Producto:
        producto = Producto(**data.dict())
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    def listar_todos(self, db: Session):
        return db.query(Producto).all()

    def obtener_por_id(self, db: Session, producto_id: int):
        return db.query(Producto).filter(Producto.id == producto_id).first()

    def eliminar(self, db: Session, producto_id: int):
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        db.delete(producto)
        db.commit()
        return {"message": "Producto eliminado"}
