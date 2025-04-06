from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.cliente_model import Cliente, ContactoCliente, DireccionEntrega, Tienda, Pedido
from src.application.schemas.clientes import ClienteCreate, ContactoClienteCreate, DireccionEntregaCreate, TiendaCreate, PedidoCreate
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