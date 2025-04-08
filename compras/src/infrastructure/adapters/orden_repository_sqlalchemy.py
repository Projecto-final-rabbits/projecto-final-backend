from sqlalchemy.orm import Session
from src.infrastructure.db.models.compra_model import OrdenCompra
from src.application.schemas.compras import OrdenCompraCreate
from fastapi import HTTPException
from src.infrastructure.db.models.compra_model import Proveedor

class OrdenCompraRepositorySQLAlchemy:
    def guardar(self, db: Session, data: OrdenCompraCreate) -> OrdenCompra:
        proveedor = db.query(Proveedor).filter(Proveedor.id == data.proveedor_id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        orden = OrdenCompra(**data.dict())
        db.add(orden)
        db.commit()
        db.refresh(orden)
        return orden

    def listar_todas(self, db: Session):
        return db.query(OrdenCompra).all()

    def obtener_por_id(self, db: Session, orden_id: int):
        return db.query(OrdenCompra).filter(OrdenCompra.id == orden_id).first()

    def eliminar(self, db: Session, orden_id: int):
        orden = self.obtener_por_id(db, orden_id)
        if orden:
            db.delete(orden)
            db.commit()
        return orden
