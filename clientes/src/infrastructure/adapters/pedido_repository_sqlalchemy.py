# src/infrastructure/adapters/pedido_repository_sqlalchemy.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.cliente_model import Pedido
from src.application.schemas.clientes import PedidoCreate

class PedidoRepositorySQLAlchemy:

    def guardar(self, db: Session, data: PedidoCreate) -> Pedido:
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
