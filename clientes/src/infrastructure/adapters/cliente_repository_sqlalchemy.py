from sqlalchemy.orm import Session
from fastapi import HTTPException
from bodegas.src.infrastructure.db.models.bodega_model import Producto
from src.infrastructure.db.models.cliente_model import Cliente
from src.application.schemas.clientes import ClienteCreate
from sqlalchemy import desc

class ClienteRepositorySQLAlchemy:
    def guardar(self, db: Session, data: ClienteCreate) -> Cliente:
        cliente = Cliente(**data.dict())
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    def listar_todos(self, db: Session):
        return db.query(Cliente).order_by(Cliente.id).all()

    def obtener_por_id(self, db: Session, cliente_id: int):
        return db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def eliminar(self, db: Session, cliente_id: int):
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        db.delete(cliente)
        db.commit()
        return {"message": "Cliente eliminado"}
    def descontar_stock(self, producto_id: int, cantidad: int) -> None:
        producto = self.db.get(Producto, producto_id)
        if not producto:
            raise ValueError(f"Producto {producto_id} no existe")

        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente ({producto.stock} < {cantidad})")

        producto.stock -= cantidad