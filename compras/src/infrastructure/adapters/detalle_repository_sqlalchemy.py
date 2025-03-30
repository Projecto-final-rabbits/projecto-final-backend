from sqlalchemy.orm import Session
from src.infrastructure.db.models.compra_model import DetalleOrdenCompra
from src.application.schemas.compras import DetalleOrdenCompraCreate
from fastapi import HTTPException
from src.infrastructure.db.models.compra_model import Producto
from src.infrastructure.db.models.compra_model import OrdenCompra

class DetalleOrdenCompraRepositorySQLAlchemy:
    def guardar(self, db: Session, data: DetalleOrdenCompraCreate) -> DetalleOrdenCompra:
        producto = db.query(Producto).filter(Producto.id == data.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        orden = db.query(OrdenCompra).filter(OrdenCompra.id == data.orden_id).first()
        if not orden:
            raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
        detalle = DetalleOrdenCompra(**data.dict())
        db.add(detalle)
        db.commit()
        db.refresh(detalle)
        return detalle

    def listar_todos(self, db: Session):
        return db.query(DetalleOrdenCompra).all()

    def obtener_por_id(self, db: Session, detalle_id: int):
        return db.query(DetalleOrdenCompra).filter(DetalleOrdenCompra.id == detalle_id).first()

    def eliminar(self, db: Session, detalle_id: int):
        detalle = self.obtener_por_id(db, detalle_id)
        if detalle:
            db.delete(detalle)
            db.commit()
        return detalle
