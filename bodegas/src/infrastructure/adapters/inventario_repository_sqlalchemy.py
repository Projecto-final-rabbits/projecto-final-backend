from src.infrastructure.db.models.bodega_model import Inventario
from sqlalchemy.orm import Session

class InventarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, inventario: Inventario):
        self.db.add(inventario)
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def obtener_todos(self):
        return self.db.query(Inventario).all()

    def obtener_por_id(self, id_: int):
        return self.db.query(Inventario).filter(Inventario.id == id_).first()

    def eliminar(self, id_: int):
        inventario = self.obtener_por_id(id_)
        if inventario:
            self.db.delete(inventario)
            self.db.commit()
            return True
        return False