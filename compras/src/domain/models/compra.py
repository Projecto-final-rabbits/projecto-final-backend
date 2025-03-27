# Modelo de dominio que representa el concepto de compra

class Compra:
    def __init__(self, producto: str, cantidad: int, proveedor: str):
        self.producto = producto
        self.cantidad = cantidad
        self.proveedor = proveedor

    def __repr__(self):
        return f"<Compra producto={self.producto} cantidad={self.cantidad} proveedor={self.proveedor}>"
