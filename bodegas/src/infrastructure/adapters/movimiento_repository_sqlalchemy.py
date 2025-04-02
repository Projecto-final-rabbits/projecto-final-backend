from src.infrastructure.db.models.bodega_model import MovimientoInventario
from sqlalchemy.orm import Session

class MovimientoInventarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, movimiento: MovimientoInventario):
        self.db.add(movimiento)
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento

    def obtener_todos(self):
        return self.db.query(MovimientoInventario).all()

    def obtener_por_id(self, id_: int):
        return self.db.query(MovimientoInventario).filter(MovimientoInventario.id == id_).first()

    def eliminar(self, id_: int):
        movimiento = self.obtener_por_id(id_)
        if movimiento:
            self.db.delete(movimiento)
            self.db.commit()
            return True
        return False
