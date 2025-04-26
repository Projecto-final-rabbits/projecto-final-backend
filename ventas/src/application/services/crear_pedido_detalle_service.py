# src/application/services/crear_pedido_con_detalle.py

import httpx
import os
from dotenv import load_dotenv

from src.application.schemas.ventas import PedidoCreate, PedidoRead, ProductoCreate
from src.infrastructure.db.models.venta_model import Pedido, DetallePedido
from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from src.infrastructure.adapters.producto_repository_sqlalchemy import ProductoRepositorySQLAlchemy
from src.infrastructure.messaging.pubsub import PubSubPublisher

load_dotenv("src/.env")
BODEGAS_BASE_URL = os.getenv("BODEGAS_BASE_URL")


class CrearPedidoConDetalleService:
    @staticmethod
    def _fetch_producto_desde_bodega(producto_id: str) -> dict:
        resp = httpx.get(f"{BODEGAS_BASE_URL}/productos/{producto_id}")
        resp.raise_for_status()
        return resp.json()

    def __init__(self, repo: PedidoRepositorySQLAlchemy):
        self.repo       = repo
        self.prod_repo  = ProductoRepositorySQLAlchemy()
        self.publisher  = PubSubPublisher()

    def execute(self, dto: PedidoCreate) -> PedidoRead:
        # 1) Crear Pedido
        pedido_orm = Pedido(
            cliente_id=       dto.cliente_id,
            vendedor_id=      dto.vendedor_id,
            fecha_envio=      dto.fecha_envio,
            direccion_entrega=dto.direccion_entrega,
            estado=           "pendiente",
        )
        self.repo.add_pedido(pedido_orm)
        db = self.repo.db

        try:
            # 2) Upsert Productos y DetallePedido
            for p in dto.productos:
                pid = p.producto_id
                local = self.prod_repo.obtener_por_id(db, pid)
                if not local:
                    data = self._fetch_producto_desde_bodega(pid)
                    schema = ProductoCreate(
                        id=              data["id"],
                        nombre=          data["nombre"],
                        descripcion=     data.get("descripcion"),
                        precio_venta=    float(data["precio_venta"]),
                        categoria=       data.get("categoria"),
                        promocion_activa=data.get("promocion_activa", False),
                    )
                    local = self.prod_repo.guardar(db, schema)
                    db.flush()

                detalle = DetallePedido(
                    pedido_id=      pedido_orm.id,
                    producto_id=    pid,
                    cantidad=       p.cantidad,
                    precio_unitario=local.precio_venta,
                )
                self.repo.add_detalle(detalle)

            # 3) Commit atómico
            self.repo.commit()

        except Exception:
            self.repo.rollback()
            raise

        # 4) Publicar eventos **por separado**
        solo_productos = [
            {"producto_id": p.producto_id, "cantidad": p.cantidad}
            for p in dto.productos
        ]

        # 4.a) lista de productos → PEDIDOS_BODEGA_TOPIC
        self.publisher.publish_productos(solo_productos)

        # 4.b) pedido completo → PEDIDO_TOPIC
        pedido_total = {
            "pedido_id":        pedido_orm.id,
            "cliente_id":       dto.cliente_id,
            "vendedor_id":      dto.vendedor_id,
            "fecha_envio":      str(dto.fecha_envio),
            "direccion_entrega":dto.direccion_entrega,
            "estado":           "pendiente",
            "productos":        solo_productos,
        }
        self.publisher.publish_pedido(pedido_total)

        # 5) Retornar DTO de lectura
        return PedidoRead(
            id=                pedido_orm.id,
            cliente_id=        pedido_orm.cliente_id,
            vendedor_id=       pedido_orm.vendedor_id,
            fecha_envio=       pedido_orm.fecha_envio,
            direccion_entrega= pedido_orm.direccion_entrega,
            estado=            pedido_orm.estado,
            productos=         dto.productos,
        )
