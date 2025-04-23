# src/application/services/crear_pedido_con_detalle.py
from src.application.schemas.ventas import PedidoCreate, PedidoRead
from src.infrastructure.db.models.venta_model import Pedido, DetallePedido
from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from src.infrastructure.adapters.out.pubsub_event_publisher import PubsubEventPublisher
from src.domain.events.event_type import EventType

class CrearPedidoConDetalleService:
    """
    • Crea el pedido
    • Inserta N registros en detalle_pedido
    • Publica dos eventos:
         EventType.bodega_product_list   → {"productos": [...]}
         EventType.clientes_pedido_total → pedido completo
    """

    def __init__(self, repo: PedidoRepositorySQLAlchemy, publisher: PubsubEventPublisher):
        self.repo = repo
        self.publisher = publisher

    def execute(self, dto: PedidoCreate) -> PedidoRead:
        # 1. Instanciar ORM Pedido
        pedido_orm = Pedido(
            cliente_id=dto.cliente_id,
            vendedor_id=dto.vendedor_id,
            fecha_envio=dto.fecha_envio,
            direccion_entrega=dto.direccion_entrega,
            estado="pendiente",
        )

        try:
            # 2. Guardar Pedido y obtener id
            self.repo.add_pedido(pedido_orm)  # flush: id ya disponible

            # 3. Insertar cada DetallePedido
            for prod in dto.productos:
                detalle = DetallePedido(
                    pedido_id=pedido_orm.id,
                    producto_id=prod.producto_id,
                    cantidad=prod.cantidad,
                )
                self.repo.add_detalle(detalle)

            # 4. Commit atómico
            self.repo.commit()

        except Exception:
            self.repo.rollback()
            raise

        # 5. Publicar eventos
        self._publish_events(dto, pedido_orm.id)

        # 6. Devolver DTO de lectura
        return PedidoRead(
            id=pedido_orm.id,
            cliente_id=pedido_orm.cliente_id,
            vendedor_id=pedido_orm.vendedor_id,
            fecha_envio=pedido_orm.fecha_envio,
            direccion_entrega=pedido_orm.direccion_entrega,
            estado=pedido_orm.estado,
            productos=dto.productos,
        )

    # --------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------
    def _publish_events(self, dto: PedidoCreate, pedido_id: int) -> None:
        # a) mensaje para BODEGA: solo lista de productos
        solo_productos = [
            {"producto_id": p.producto_id, "cantidad": p.cantidad}
            for p in dto.productos
        ]
        self.publisher.publish(EventType.bodega_product_list, {"productos": solo_productos})

        # b) mensaje para CLIENTES: pedido completo
        pedido_total = {
            "pedido_id": pedido_id,
            "cliente_id": dto.cliente_id,
            "vendedor_id": dto.vendedor_id,
            "fecha_envio": str(dto.fecha_envio),
            "direccion_entrega": dto.direccion_entrega,
            "estado": "pendiente",
            "productos": solo_productos,
        }
        self.publisher.publish(EventType.clientes_pedido_total, pedido_total)

        # c) (opcional) mantiene el evento histórico
        self.publisher.publish(EventType.pedido_created, pedido_total)
