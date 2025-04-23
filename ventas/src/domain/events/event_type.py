from enum import Enum

class EventType(str, Enum):
    pedido_selled = "pedido-selled"
    pedido_updated = "pedido-updated"
    pedido_created = "pedido-created"

    # ----- NUEVOS eventos -----
    bodega_product_list   = "bodega-product-list"     # → solo lista de productos
    clientes_pedido_total = "clientes-pedido-total"   # → pedido completo (con productos)