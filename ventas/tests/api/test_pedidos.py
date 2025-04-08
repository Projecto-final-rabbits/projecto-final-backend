def test_crear_cliente_para_pedido(client):
    response = client.post("/clientes/", json={
        "nombre": "Cliente Pedido",
        "tipo_cliente": "minorista",
        "direccion": "Cra 10 #12-34",
        "telefono": "3004567890",
        "email": "cliente@correo.com"
    })
    assert response.status_code == 200

def test_crear_vendedor_para_pedido(client):
    response = client.post("/vendedores/", json={
        "nombre": "Vendedor Pedido",
        "zona": "Sur",
        "telefono": "3216549870",
        "email": "vendedor@correo.com"
    })
    assert response.status_code == 200

def test_crear_pedido(client):
    response = client.post("/pedidos/", json={
        "cliente_id": 1,
        "vendedor_id": 1,
        "fecha_pedido": "2025-04-01",
        "estado": "pendiente",
        "total": 250.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["cliente_id"] == 1
    assert data["estado"] == "pendiente"

def test_listar_pedidos(client):
    response = client.get("/pedidos/")
    assert response.status_code == 200
    pedidos = response.json()
    assert isinstance(pedidos, list)
    assert any(p["estado"] == "pendiente" for p in pedidos)

def test_obtener_pedido(client):
    response = client.get("/pedidos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_eliminar_pedido(client):
    response = client.delete("/pedidos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Pedido eliminado"
