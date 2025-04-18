from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy

class PedidoService:
    def __init__(self, event_publisher, repo: PedidoRepositorySQLAlchemy):
        self.event_publisher = event_publisher
        self.repo = repo
    
    def crear_pedido_event(self, pedido: dict ):

        from src.domain.events.event_type import EventType
        self.event_publisher.publish(EventType.pedido_created, pedido)
        # Publicar el evento de creación de pedido


    