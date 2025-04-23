import os
from dotenv import load_dotenv
import httpx
from src.config.database import get_db

load_dotenv("src/.env")

CLIENTES_BASE_URL = os.getenv("CLIENTES_BASE_URL")


def direccion_entrega_existe(direccion_entrega_id: int) -> bool:
    try:
        response = httpx.get(f"{CLIENTES_BASE_URL}/direcciones/{direccion_entrega_id}")
        return response.status_code == 200
    except httpx.RequestError:
        return False
