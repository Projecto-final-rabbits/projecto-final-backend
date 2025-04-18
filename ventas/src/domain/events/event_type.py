from enum import Enum

class EventType(str, Enum):
    pedido_selled = "pedido-selled"
    pedido_updated = "pedido-updated"
    pedido_created = "pedido-created"