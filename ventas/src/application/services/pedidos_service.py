# ventas/src/application/services/pedidos_service.py

import os
import requests
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.application.schemas.ruta import DireccionesPedido
from src.infrastructure.db.models.venta_model import Pedido

# Leemos la URL base del MS de Bodegas desde una variable de entorno
BODEGAS_URL = os.getenv("BODEGAS_BASE_URL", "http://bodegas-service:8003")

def obtener_direcciones_pedido_service(pedido_id: int, db: Session) -> DireccionesPedido:
    # 1) Recuperar el pedido
    pedido: Pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # 2) Llamar al MS de Bodegas
    url = f"{BODEGAS_URL}/bodegas/{pedido.origen_bodega_id}"
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Error conectando a Bodegas: {e}")

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="No se pudo obtener la bodega de origen")

    bodega_data = resp.json()
    origen = bodega_data.get("direccion") or f"{bodega_data['ciudad']}, {bodega_data['pais']}"
    destino = pedido.direccion_entrega

    return DireccionesPedido(pedido_id=pedido_id, origen=origen, destino=destino)
