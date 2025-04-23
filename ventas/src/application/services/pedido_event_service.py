from src.domain.events.event_type import EventType
from src.infrastructure.adapters.out.pubsub_event_publisher import PubsubEventPublisher

class PedidoService:
    def __init__(self, publisher: PubsubEventPublisher):
        self.publisher = publisher

    # --- evento clásico (si lo sigues usando)
    def crear_pedido_event(self, pedido: dict):
        self.publisher.publish(EventType.pedido_created, pedido)

    # --- nuevos flujos para creación de pedido
    def publicar_eventos_pedido(self, pedido_total: dict, solo_productos: list[dict]) -> None:
        # 1. Bodega → solo lista de productos
        self.publisher.publish(EventType.bodega_product_list, {"productos": solo_productos})
        # 2. Clientes → pedido completo
        self.publisher.publish(EventType.clientes_pedido_total, pedido_total)
        # 3. (opcional) mantener tu evento histórico
        self.publisher.publish(EventType.pedido_created, pedido_total)
