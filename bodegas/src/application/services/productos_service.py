from src.application.ports.out.event_publisher import EventPublisher
from src.domain.events.event_type import EventType

class ProductosService:
    def __init__(self, event_publisher: EventPublisher):
        self.event_publisher = event_publisher

    def crear_producto(self, producto: dict):
        self.event_publisher.publish(EventType.product_created, producto)

