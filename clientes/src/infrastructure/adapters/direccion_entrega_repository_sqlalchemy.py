from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.cliente_model import DireccionEntrega
from src.application.schemas.clientes import DireccionEntregaCreate

class DireccionEntregaRepositorySQLAlchemy:
    def guardar(self, db: Session, data: DireccionEntregaCreate) -> DireccionEntrega:
        direccion = DireccionEntrega(**data.dict())
        db.add(direccion)
        db.commit()
        db.refresh(direccion)
        return direccion

    def listar_todos(self, db: Session):
        return db.query(DireccionEntrega).all()

    def obtener_por_id(self, db: Session, direccion_id: int):
        return db.query(DireccionEntrega).filter(DireccionEntrega.id == direccion_id).first()

    def eliminar(self, db: Session, direccion_id: int):
        direccion = db.query(DireccionEntrega).filter(DireccionEntrega.id == direccion_id).first()
        if not direccion:
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        db.delete(direccion)
        db.commit()
        return {"message": "Dirección eliminada"}
