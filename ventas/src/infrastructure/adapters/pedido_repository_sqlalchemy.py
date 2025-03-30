from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import Pedido, Cliente, Vendedor
from src.application.schemas.ventas import PedidoCreate

class PedidoRepositorySQLAlchemy:
    def guardar(self, db: Session, data: PedidoCreate) -> Pedido:
        if not db.query(Cliente).filter(Cliente.id == data.cliente_id).first():
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        if not db.query(Vendedor).filter(Vendedor.id == data.vendedor_id).first():
            raise HTTPException(status_code=404, detail="Vendedor no encontrado")
        pedido = Pedido(**data.dict())
        db.add(pedido)
        db.commit()
        db.refresh(pedido)
        return pedido

    def listar_todos(self, db: Session):
        return db.query(Pedido).all()

    def obtener_por_id(self, db: Session, pedido_id: int):
        return db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def eliminar(self, db: Session, pedido_id: int):
        pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        db.delete(pedido)
        db.commit()
        return {"message": "Pedido eliminado"}
