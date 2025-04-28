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

    def obtener_por_producto(self, producto_id: str) -> Inventario | None:
        return (
            self.db
            .query(Inventario)
            .filter(Inventario.producto_id == producto_id)
            .first()
        )

    def descontar_stock(self, producto_id: str, cantidad: int) -> None:
        inventario = self.obtener_por_producto(producto_id)
        if not inventario:
            raise ValueError(f"No existe inventario para el producto {producto_id}")

        if inventario.cantidad_disponible < cantidad:
            raise ValueError(
                f"Stock insuficiente para producto {producto_id} "
                f"(disponible: {inventario.cantidad_disponible}, solicitado: {cantidad})"
            )

        inventario.cantidad_disponible -= cantidad

        # TODO: registrar MovimientoInventario aquí
        # movimiento = MovimientoInventario(
        #     producto_id=inventario.producto_id,
        #     bodega_id=inventario.bodega_id,
        #     tipo_movimiento=TipoMovimientoEnum.salida,
        #     cantidad=cantidad,
        #     fecha=date.today(),
        #     descripcion="Salida por pedido (Pub/Sub)"
        # )
        # self.db.add(movimiento)
    
    def obtener_por_producto_y_bodega(self, producto_id, bodega_id):
        return self.db.query(Inventario).filter(
            Inventario.producto_id == producto_id,
            Inventario.bodega_id == bodega_id
        ).first()

    def actualizar(self, inventario: Inventario):
        self.db.add(inventario)
        self.db.commit()
        self.db.refresh(inventario)
        return inventario
