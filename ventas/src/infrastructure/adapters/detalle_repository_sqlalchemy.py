from datetime import date
from typing import List, Tuple
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.infrastructure.db.models.venta_model import DetallePedido, Pedido, Producto
from src.application.schemas.ventas import DetallePedidoCreate

class DetallePedidoRepositorySQLAlchemy:
    def guardar(self, db: Session, data: DetallePedidoCreate) -> DetallePedido:
        if not db.query(Pedido).filter(Pedido.id == data.pedido_id).first():
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        if not db.query(Producto).filter(Producto.id == data.producto_id).first():
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        detalle = DetallePedido(**data.dict())
        db.add(detalle)
        db.commit()
        db.refresh(detalle)
        return detalle

    def listar_todos(self, db: Session):
        return db.query(DetallePedido).all()

    def obtener_por_id(self, db: Session, detalle_id: int):
        return db.query(DetallePedido).filter(DetallePedido.id == detalle_id).first()

    def eliminar(self, db: Session, detalle_id: int):
        detalle = db.query(DetallePedido).filter(DetallePedido.id == detalle_id).first()
        if not detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        db.delete(detalle)
        db.commit()
        return {"message": "Detalle eliminado"}
    
    def ventas_por_cliente(
            self,
            db: Session,
            cliente_id: int,
            fecha_inicio: date,
            fecha_fin: date
        ) -> List[Tuple[str, int, float]]:
            """
            Devuelve una lista de tuplas:
            (nombre_producto, cantidad_total, total_ventas)
            """
            q = (
                db.query(
                    Producto.nombre.label("nombre"),
                    func.sum(DetallePedido.cantidad).label("cantidad_total"),
                    func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario).label("total_ventas"),
                )
                .join(DetallePedido.pedido)          # une con Pedido
                .join(DetallePedido.producto)        # une con Producto
                .filter(
                    Pedido.cliente_id == cliente_id,
                    Pedido.fecha_envio >= fecha_inicio,
                    Pedido.fecha_envio <= fecha_fin,
                )
                .group_by(Producto.nombre)
            )
            return q.all()
        
    def obtener_por_pedido(self, db: Session, pedido_id: int) -> List[DetallePedido]:
        """
        Devuelve todos los DetallePedido asociados a un pedido dado su ID.
        """
        return (
            db
            .query(DetallePedido)
            .filter(DetallePedido.pedido_id == pedido_id)
            .all()
        )