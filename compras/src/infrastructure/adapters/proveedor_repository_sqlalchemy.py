from sqlalchemy.orm import Session
from src.infrastructure.db.models.compra_model import Proveedor
from src.application.schemas.compras import ProveedorCreate

class ProveedorRepositorySQLAlchemy:
    def guardar(self, db: Session, data: ProveedorCreate) -> Proveedor:
        proveedor = Proveedor(**data.dict())
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)
        return proveedor

    def listar_todos(self, db: Session):
        return db.query(Proveedor).all()

    def obtener_por_id(self, db: Session, proveedor_id: int):
        return db.query(Proveedor).filter(Proveedor.id == proveedor_id).first()

    def eliminar(self, db: Session, proveedor_id: int):
        proveedor = self.obtener_por_id(db, proveedor_id)
        if proveedor:
            db.delete(proveedor)
            db.commit()
        return proveedor
