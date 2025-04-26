from enum import Enum

class EventType(str, Enum):
    product_selled = "product-selled"
    product_updated = "product-updated"
    product_created = "product-created"
    product_sync_ventas = "product-sync-ventas"