from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import Pedido, Cliente, Vendedor
from src.application.schemas.ventas import PedidoCreate

class PedidoRepositorySQLAlchemy:

    def __init__(self, db: Session):
        self.db = db

    def guardar(self, data: PedidoCreate) -> Pedido:
        if not self.db.query(Cliente).filter(Cliente.id == data.cliente_id).first():
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        if not self.db.query(Vendedor).filter(Vendedor.id == data.vendedor_id).first():
            raise HTTPException(status_code=404, detail="Vendedor no encontrado")
        pedido = Pedido(**data.dict())
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

    def listar_todos(self):
        return self.db.query(Pedido).all()

    def obtener_por_id(self, pedido_id: int):
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def eliminar(self, pedido_id: int):
        pedido = self.db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        self.db.delete(pedido)
        self.db.commit()
        return {"message": "Pedido eliminado"}
