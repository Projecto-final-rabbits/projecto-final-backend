from sqlalchemy.orm import Session
from src.infrastructure.db.models.compra_model import Producto
from src.application.schemas.compras import ProductoCreate
from fastapi import HTTPException
from src.infrastructure.db.models.compra_model import Proveedor

class ProductoRepositorySQLAlchemy:
    def guardar(self, db: Session, data: ProductoCreate) -> Producto:
        proveedor = db.query(Proveedor).filter(Proveedor.id == data.proveedor_id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
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
        producto = self.obtener_por_id(db, producto_id)
        if producto:
            db.delete(producto)
            db.commit()
        return producto

    def listar_por_pais(self, db: Session, pais: str):
        return (
            db.query(Producto)
            .join(Proveedor, Producto.proveedor_id == Proveedor.id)
            .filter(Proveedor.pais == pais)
            .all()
        )