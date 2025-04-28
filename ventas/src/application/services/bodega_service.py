from uuid import UUID
import httpx
import os
from dotenv import load_dotenv

from src.application.schemas.ventas import ProductoRead

load_dotenv("src/.env")
BODEGAS_BASE_URL = os.getenv("BODEGAS_BASE_URL")  # e.g. http://bodegas:8003

def producto_en_stock(product_id: UUID, cantidad_solicitada: int) -> bool:
    """
    Devuelve True si la cantidad disponible en inventario
    es mayor o igual a la cantidad solicitada.
    """
    url = f"{BODEGAS_BASE_URL}/inventarios/producto/{product_id}"
    try:
        resp = httpx.get(url, timeout=5.0)
        if resp.status_code == 200:
            data = resp.json()
            cantidad_disponible = data.get("cantidad_disponible", 0)
            return cantidad_disponible >= cantidad_solicitada

        elif resp.status_code == 404:
            # No hay inventario registrado para este producto
            return False

        else:
            resp.raise_for_status()

    except httpx.RequestError as e:
        print(f"🚨 Error de red al consultar inventario: {e}")
        return False
    except Exception as e:
        print(f"🚨 Error inesperado al verificar stock: {e}")
        return False

def fetch_producto(product_id: UUID) -> ProductoRead:
    url = f"{BODEGAS_BASE_URL}/productos/{product_id}"
    resp = httpx.get(url, timeout=5.0)
    resp.raise_for_status()   # lanza HTTPError si no es 200
    return ProductoRead(**resp.json())