import httpx

COMPRAS_BASE_URL = "https://compras-135751842587.us-central1.run.app"  # Agregar variable de entorno en github secrets

def proveedor_existe(proveedor_id: int) -> bool:
    try:
        response = httpx.get(f"{COMPRAS_BASE_URL}/proveedores/{proveedor_id}")
        return response.status_code == 200
    except httpx.RequestError:
        return False
