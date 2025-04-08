from src.infrastructure.db.models.bodega_model import Bodega
from sqlalchemy.orm import Session

class BodegaRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, bodega: Bodega):
        self.db.add(bodega)
        self.db.commit()
        self.db.refresh(bodega)
        return bodega

    def obtener_todas(self):
        return self.db.query(Bodega).all()

    def obtener_por_id(self, id_: int):
        return self.db.query(Bodega).filter(Bodega.id == id_).first()

    def eliminar(self, id_: int):
        bodega = self.obtener_por_id(id_)
        if bodega:
            self.db.delete(bodega)
            self.db.commit()
            return True
        return False