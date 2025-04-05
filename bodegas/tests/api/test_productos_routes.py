import io
import pandas as pd
from unittest.mock import patch
import httpx

def test_cargar_csv_productos_exitoso(client):
    # Crear CSV con 2 productos válidos
    df = pd.DataFrame([
        {
            "nombre": "Aceite Test",
            "descripcion": "Test aceite",
            "categoria": "Alimentos",
            "proveedor_id": 1,
            "precio_compra": 2.0,
            "precio_venta": 4.0,
            "promocion_activa": True,
            "fecha_vencimiento": "2025-12-31",
            "condicion_almacenamiento": "Ambiente seco",
            "tiempo_entrega_dias": 3
        },
        {
            "nombre": "Galletas Test",
            "descripcion": "Test galletas",
            "categoria": "Dulces",
            "proveedor_id": 1,
            "precio_compra": 1.5,
            "precio_venta": 3.0,
            "promocion_activa": False,
            "fecha_vencimiento": "",
            "condicion_almacenamiento": "Caja cerrada",
            "tiempo_entrega_dias": 5
        }
    ])
    csv_bytes = df.to_csv(index=False).encode("utf-8") 
    file_stream = io.BytesIO(csv_bytes)

    response = client.post(
        "/productos/masivo",
        files={"file": ("productos.csv", file_stream, "text/csv")}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["creados"] == 2
    assert data["fallos"] == 0

def test_csv_producto_con_proveedor_invalido(client):
    df = pd.DataFrame([
        {
            "nombre": "Producto Invalido",
            "descripcion": "No válido",
            "categoria": "Otros",
            "proveedor_id": 9999,  # No existe
            "precio_compra": 1.0,
            "precio_venta": 2.0,
            "promocion_activa": True,
            "fecha_vencimiento": "",
            "condicion_almacenamiento": "Ambiente seco",
            "tiempo_entrega_dias": 4
        }
    ])
    csv_bytes = df.to_csv(index=False).encode("utf-8")  
    file_stream = io.BytesIO(csv_bytes)

    response = client.post(
        "/productos/masivo",
        files={"file": ("invalid.csv", file_stream, "text/csv")}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["creados"] == 0
    assert data["fallos"] == 1
    assert "Proveedor" in data["errores"][0]["error"]

@patch("src.infrastructure.adapters.out.pubsub_event_publisher.PubsubEventPublisher.publish")
def test_csv_pubsub_mockeado(mock_publish, client):
    mock_publish.return_value = True  # Simula éxito

    # CSV válido
    df = pd.DataFrame([
        {
            "nombre": "Producto PubSub Test",
            "descripcion": "Test",
            "categoria": "Test",
            "proveedor_id": 1,
            "precio_compra": 1.0,
            "precio_venta": 2.0,
            "promocion_activa": False,
            "fecha_vencimiento": "",
            "condicion_almacenamiento": "Caja",
            "tiempo_entrega_dias": 5
        }
    ])
    csv_bytes = df.to_csv(index=False).encode("utf-8")  
    file_stream = io.BytesIO(csv_bytes)

    response = client.post(
        "/productos/masivo",
        files={"file": ("pubsub.csv", file_stream, "text/csv")}
    )

    assert response.status_code == 201
    assert mock_publish.called

def test_listar_productos(client):
    response = client.get("/productos/")
    assert response.status_code == 200
    productos = response.json()
    assert isinstance(productos, list)
    assert len(productos) >= 1  

def test_crear_producto_unitario(client):
    payload = {
        "nombre": "Producto Test Unitario",
        "descripcion": "Producto para test POST",
        "categoria": "Test",
        "proveedor_id": 1,
        "precio_compra": 1.5,
        "precio_venta": 2.5,
        "promocion_activa": True,
        "fecha_vencimiento": "2025-12-31",
        "condicion_almacenamiento": "Ambiente seco",
        "tiempo_entrega_dias": 4
    }

    response = client.post("/productos/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["precio_venta"] == payload["precio_venta"]

def test_obtener_producto_por_id(client):
    # Crear producto
    payload = {
        "nombre": "Producto Consulta",
        "descripcion": "Producto para GET por ID",
        "categoria": "Consulta",
        "proveedor_id": 1,
        "precio_compra": 2.0,
        "precio_venta": 3.5,
        "promocion_activa": False,
        "fecha_vencimiento": "2025-11-30",
        "condicion_almacenamiento": "Caja",
        "tiempo_entrega_dias": 6
    }
    crear_resp = client.post("/productos/", json=payload)
    assert crear_resp.status_code == 200
    print(crear_resp, "respuesta de la creacion")
    producto_creado = crear_resp.json()

    # Consultar por ID
    response = client.get(f"/productos/{producto_creado['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == payload["nombre"]

def test_eliminar_producto_por_id(client):
    # Crear producto
    payload = {
        "nombre": "Producto Eliminable",
        "descripcion": "Producto a borrar",
        "categoria": "Eliminar",
        "proveedor_id": 1,
        "precio_compra": 1.2,
        "precio_venta": 2.4,
        "promocion_activa": False,
        "fecha_vencimiento": "2025-10-10",
        "condicion_almacenamiento": "Caja",
        "tiempo_entrega_dias": 2
    }
    crear_resp = client.post("/productos/", json=payload)
    assert crear_resp.status_code == 200
    producto_id = crear_resp.json()["id"]

    # Eliminar
    delete_resp = client.delete(f"/productos/{producto_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Producto eliminado correctamente"

    # Verificar que ya no existe
    get_resp = client.get(f"/productos/{producto_id}")
    assert get_resp.status_code == 404
