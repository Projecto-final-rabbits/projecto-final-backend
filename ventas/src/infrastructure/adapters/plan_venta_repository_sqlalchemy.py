from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import PlanVenta, Vendedor, Producto
from src.application.schemas.ventas import PlanVentaCreate

class PlanVentaRepositorySQLAlchemy:
    def guardar(self, db: Session, data: PlanVentaCreate) -> PlanVenta:
        if not db.query(Vendedor).filter(Vendedor.id == data.vendedor_id).first():
            raise HTTPException(status_code=404, detail="Vendedor no encontrado")
        if not db.query(Producto).filter(Producto.id == data.producto_id).first():
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        plan = PlanVenta(**data.dict())
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan

    def listar_todos(self, db: Session):
        return db.query(PlanVenta).all()

    def obtener_por_id(self, db: Session, plan_id: int):
        return db.query(PlanVenta).filter(PlanVenta.id == plan_id).first()

    def eliminar(self, db: Session, plan_id: int):
        plan = db.query(PlanVenta).filter(PlanVenta.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan de venta no encontrado")
        db.delete(plan)
        db.commit()
        return {"message": "Plan de venta eliminado"}
