import httpx
import os
from dotenv import load_dotenv

load_dotenv("src/.env")

COMPRAS_BASE_URL = os.getenv("COMPRAS_BASE_URL")

def proveedor_existe(proveedor_id: int) -> bool:
    try:
        response = httpx.get(f"{COMPRAS_BASE_URL}/proveedores/{proveedor_id}")
        return response.status_code == 200
    except httpx.RequestError:
        return False
