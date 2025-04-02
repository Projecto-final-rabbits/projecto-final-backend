from src.infrastructure.db.models.bodega_model import Producto
from sqlalchemy.orm import Session

class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, producto: Producto):
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_todos(self):
        return self.db.query(Producto).all()

    def obtener_por_id(self, id_: str):
        return self.db.query(Producto).filter(Producto.id == id_).first()

    def eliminar(self, id_: str):
        producto = self.obtener_por_id(id_)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False