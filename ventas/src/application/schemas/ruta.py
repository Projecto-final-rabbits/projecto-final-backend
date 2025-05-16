# ventas/src/application/schemas/ruta.py

from pydantic import BaseModel

class DireccionesPedido(BaseModel):
    pedido_id: int
    origen: str
    destino: str

    class Config:
        from_attributes = True