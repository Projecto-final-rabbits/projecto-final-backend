from fastapi import HTTPException
from src.infrastructure.db.models.bodega_model import Producto
from sqlalchemy.orm import Session
from uuid import UUID

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
        if isinstance(id_, str):
            id_ = UUID(id_)
        return self.db.query(Producto).filter(Producto.id == id_).first()

    def eliminar(self, id_: str):
        if isinstance(id_, str):
            id_ = UUID(id_)
        producto = self.db.query(Producto).filter(Producto.id == id_).first()
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
    
    def obtener_por_proveedor(self, proveedor_id: int):
        return self.db.query(Producto).filter(Producto.proveedor_id == str(proveedor_id)).all()
    
    
    def descontar_stock(self, producto_id: int, cantidad: int) -> None:
        producto = self.db.get(Producto, producto_id)
        if not producto:
            raise ValueError(f"Producto {producto_id} no existe")

        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente ({producto.stock} < {cantidad})")

        producto.stock -= cantidad
        # No commit aquí: lo hace el calle
    def eliminar_todos(self):
        self.db.query(Producto).delete()
        self.db.commit()

    def obtener_por_nombre(self, nombre: str):
        return self.db.query(Producto).filter(Producto.nombre == nombre).first()
    
    def obtener_por_categoria(self, categoria: str):
        return self.db.query(Producto).filter(Producto.categoria == categoria).all()

    def obtener_por_proveedor_y_categoria(self, proveedor_id: int, categoria: str):
        return self.db.query(Producto).filter(
            Producto.proveedor_id == str(proveedor_id),
            Producto.categoria == categoria
        ).all()

    def actualizar(self, id_: str, campos: dict):
        """
        Actualiza sólo los campos que vienen en `campos`.
        """
        producto = self.obtener_por_id(id_)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        for attr, valor in campos.items():
            setattr(producto, attr, valor)
        self.db.commit()
        self.db.refresh(producto)
        return producto