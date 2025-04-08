def test_crear_cliente_y_vendedor_para_detalle(client):
    # Cliente
    response = client.post("/clientes/", json={
        "nombre": "Cliente Detalle",
        "tipo_cliente": "mayorista",
        "direccion": "Av Siempre Viva",
        "telefono": "1234567890",
        "email": "cliente@detalle.com"
    })
    assert response.status_code == 200

    # Vendedor
    response = client.post("/vendedores/", json={
        "nombre": "Vendedor Detalle",
        "zona": "Centro",
        "telefono": "0987654321",
        "email": "vendedor@detalle.com"
    })
    assert response.status_code == 200

def test_crear_producto_para_detalle(client):

    # Producto
    response = client.post("/productos/", json={
        "nombre": "Mouse",
        "descripcion": "Mouse óptico",
        "precio_venta": 50.0,
        "stock": 100,
        "categoria": "Periféricos",
        "proveedor_id": 1
    })
    assert response.status_code == 200

def test_crear_pedido_para_detalle(client):
    response = client.post("/pedidos/", json={
        "cliente_id": 1,
        "vendedor_id": 1,
        "fecha_pedido": "2025-04-02",
        "estado": "pendiente",
        "total": 50.0
    })
    assert response.status_code == 200

def test_crear_detalle_pedido(client):
    response = client.post("/detalles/", json={
        "pedido_id": 1,
        "producto_id": 1,
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
