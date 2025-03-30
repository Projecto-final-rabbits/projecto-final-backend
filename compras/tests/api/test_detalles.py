proveedor_id = None
producto_id = None
orden_id = None
detalle_id = None

def test_crear_proveedor(client):
    global proveedor_id
    response = client.post("/proveedores/", json={
        "nombre": "Proveedor Detalle",
        "pais": "Chile",
        "contacto": "Laura Mendoza",
        "telefono": "3001234567",
        "email": "proveedor_detalle@test.com"
    })
    assert response.status_code == 200
    proveedor_id = response.json()["id"]

def test_crear_producto(client):
    global producto_id
    response = client.post("/productos/", json={
        "nombre": "Producto Detalle",
        "descripcion": "Para test detalle",
        "precio_compra": 30000.0,
        "categoria": "Oficina",
        "tiempo_entrega_dias": 5,
        "proveedor_id": proveedor_id
    })
    assert response.status_code == 200
    producto_id = response.json()["id"]

def test_crear_orden(client):
    global orden_id
    response = client.post("/ordenes/", json={
        "proveedor_id": proveedor_id,
        "estado": "pendiente",
        "total": 0.0
    })
    assert response.status_code == 200
    orden_id = response.json()["id"]

def test_crear_detalle_con_producto_inexistente(client):
    test_crear_proveedor(client)
    test_crear_orden(client)
    
    response = client.post("/detalles/", json={
        "orden_id": orden_id,
        "producto_id": 9999,
        "cantidad": 3,
        "precio_unitario": 20000.0
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Producto no encontrado"

def test_crear_detalle_con_orden_inexistente(client):
    test_crear_proveedor(client)
    test_crear_producto(client)

    response = client.post("/detalles/", json={
        "orden_id": 9999,
        "producto_id": producto_id,
        "cantidad": 2,
        "precio_unitario": 10000.0
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Orden de compra no encontrada"


def test_crear_detalle(client):
    global detalle_id
    response = client.post("/detalles/", json={
        "orden_id": orden_id,
        "producto_id": producto_id,
        "cantidad": 4,
        "precio_unitario": 30000.0
    })
    assert response.status_code == 200
    detalle_id = response.json()["id"]

def test_listar_detalles(client):
    response = client.get("/detalles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_detalle(client):
    response = client.get(f"/detalles/{detalle_id}")
    assert response.status_code == 200
    assert response.json()["id"] == detalle_id

def test_eliminar_detalle(client):
    response = client.delete(f"/detalles/{detalle_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Detalle eliminado"

def test_eliminar_orden(client):
    response = client.delete(f"/ordenes/{orden_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Orden eliminada"

def test_eliminar_producto(client):
    response = client.delete(f"/productos/{producto_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Producto eliminado"

def test_eliminar_proveedor(client):
    response = client.delete(f"/proveedores/{proveedor_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Proveedor eliminado"
