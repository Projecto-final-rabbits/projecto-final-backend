from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.cliente_model import Tienda
from src.application.schemas.clientes import TiendaCreate

class TiendaRepositorySQLAlchemy:
    def guardar(self, db: Session, data: TiendaCreate) -> Tienda:
        tienda = Tienda(**data.dict())
        db.add(tienda)
        db.commit()
        db.refresh(tienda)
        return tienda

    def listar_todos(self, db: Session):
        return db.query(Tienda).all()

    def obtener_por_id(self, db: Session, tienda_id: int):
        return db.query(Tienda).filter(Tienda.id == tienda_id).first()

    def eliminar(self, db: Session, tienda_id: int):
        tienda = db.query(Tienda).filter(Tienda.id == tienda_id).first()
        if not tienda:
            raise HTTPException(status_code=404, detail="Tienda no encontrada")
        db.delete(tienda)
        db.commit()
        return {"message": "Tienda eliminada"}
    
