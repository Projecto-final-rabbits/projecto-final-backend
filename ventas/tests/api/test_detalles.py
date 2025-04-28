def crear_cliente_vendedor_pedido_producto(client):
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
        "fecha_envio": "2025-04-02",
        "direccion_entrega": "Av Siempre Viva",
        "productos": [],
        "estado": "pendiente",
        "total": 50.0
    })
    assert response.status_code == 201
    pedido_id = response.json()["id"]

    # Crear producto
    response = client.post("/productos/", json={
        "nombre": "Mouse",
        "descripcion": "Mouse óptico",
        "precio_venta": 50.0,
        "categoria": "Periféricos",
        "promocion_activa": False
    })
    assert response.status_code == 200
    producto_id = response.json()["id"]

    return pedido_id, producto_id

def test_crear_detalle_pedido(client):
    pedido_id, producto_id = crear_cliente_vendedor_pedido_producto(client)
    response = client.post("/detalles/", json={
        "pedido_id": pedido_id,
        "producto_id": producto_id,
        "cantidad": 2,
        "precio_unitario": 50.0
    })
    # assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 2
    assert data["pedido_id"] == pedido_id
    assert data["producto_id"] == producto_id

# def test_listar_detalles(client):
#     response = client.get("/detalles/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_obtener_detalle(client):
#     pedido_id, producto_id = crear_cliente_vendedor_pedido_producto(client)
#     client.post("/detalles/", json={
#         "pedido_id": pedido_id,
#         "producto_id": producto_id,
#         "cantidad": 2,
#         "precio_unitario": 50.0
#     })
#     response = client.get("/detalles/1")
#     assert response.status_code == 201
#     data = response.json()
#     assert data["id"] == 1

# def test_eliminar_detalle(client):
#     pedido_id, producto_id = crear_cliente_vendedor_pedido_producto(client)
#     client.post("/detalles/", json={
#         "pedido_id": pedido_id,
#         "producto_id": producto_id,
#         "cantidad": 2,
#         "precio_unitario": 50.0
#     })
#     response = client.delete("/detalles/1")
#     assert response.status_code == 201
#     data = response.json()
#     assert data["message"] == "Detalle eliminado"
