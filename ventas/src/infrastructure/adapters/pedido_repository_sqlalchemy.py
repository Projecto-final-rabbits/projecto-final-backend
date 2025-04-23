from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import DetallePedido, Pedido
from src.application.schemas.ventas import PedidoCreate

class PedidoRepositorySQLAlchemy:

    def __init__(self, db: Session):
        self.db = db

# src/infrastructure/adapters/pedido_repository_sqlalchemy.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import Pedido
from src.application.schemas.ventas import PedidoCreate

class PedidoRepositorySQLAlchemy:

    def __init__(self, db: Session):
        self.db = db

        # ---------- Pedido ----------
    def add_pedido(self, pedido: Pedido) -> Pedido:
        self.db.add(pedido)
        self.db.flush()        # genera id sin cerrar la transacción
        return pedido

    # ---------- Detalle ----------
    def add_detalle(self, detalle: DetallePedido) -> DetallePedido:
        self.db.add(detalle)
        return detalle

    # ---------- utilidades ----------
    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def listar_todos(self) -> list[Pedido]:
        return self.db.query(Pedido).all()

    def obtener_por_id(self, pedido_id: int) -> Pedido | None:
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def eliminar(self, pedido_id: int) -> dict:
        pedido = self.db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        self.db.delete(pedido)
        self.db.commit()
        return {"message": "Pedido eliminado"}
