import httpx

COMPRAS_BASE_URL = "http://compras:8000"  # o la URL pública si estás en producción

def proveedor_existe(proveedor_id: int) -> bool:
    try:
        response = httpx.get(f"{COMPRAS_BASE_URL}/proveedores/{proveedor_id}")
        return response.status_code == 200
    except httpx.RequestError:
        return False
