def test_crear_cliente_y_vendedor_para_detalle(client):
    # Crear cliente
    response = client.post("/clientes/", json={
        "nombre": "Cliente Detalle",
        "tipo_cliente": "mayorista",
        "direccion": "Av Siempre Viva",
        "telefono": "1234567890",
        "email": "cliente@detalle.com"
    })
    assert response.status_code == 200
    cliente_id = response.json()["id"]

    # Crear vendedor
    response = client.post("/vendedores/", json={
        "nombre": "Vendedor Detalle",
        "zona": "Centro",
        "telefono": "0987654321",
        "email": "vendedor@detalle.com"
    })
    assert response.status_code == 200
    vendedor_id = response.json()["id"]

    # Crear pedido
    response = client.post("/pedidos/", json={
        "cliente_id": cliente_id,
        "vendedor_id": vendedor_id,
        "fecha": "2025-04-02",
        "estado": "pendiente",
        "total": 50.0
    })
    assert response.status_code == 200
    global pedido_id
    pedido_id = response.json()["id"]

def test_crear_producto_para_detalle(client):
    # Crear producto
    response = client.post("/productos/", json={
        "nombre": "Mouse",
        "descripcion": "Mouse óptico",
        "precio_venta": 50.0,
        "categoria": "Periféricos",
        "promocion_activa": False
    })
    assert response.status_code == 200
    global producto_id
    producto_id = response.json()["id"]

def test_crear_detalle_pedido(client):
    response = client.post("/detalles/", json={
        "pedido_id": pedido_id,
        "producto_id": producto_id,
        "cantidad": 2,
        "precio_unitario": 50.0
    })
    assert response.status_code == 200
    assert response.json()["cantidad"] == 2

def test_listar_detalles(client):
    response = client.get("/detalles/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_detalle(client):
    response = client.get("/detalles/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_eliminar_detalle(client):
    response = client.delete("/detalles/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Detalle eliminado"
