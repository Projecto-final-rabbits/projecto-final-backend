def test_crear_vendedor_y_producto_para_plan(client):
    global vendedor_id, producto_id

    # Vendedor
    response = client.post("/vendedores/", json={
        "nombre": "Vendedor Plan",
        "zona": "Occidente",
        "telefono": "3003003000",
        "email": "vendedor@plan.com"
    })
    assert response.status_code == 200
    vendedor_id = response.json()["id"]

    # Producto
    response = client.post("/productos/", json={
        "nombre": "Monitor",
        "descripcion": "Monitor Full HD",
        "precio_venta": 800.0,
        "categoria": "Pantallas",
        "promocion_activa": False
    })
    assert response.status_code == 200
    producto_id = response.json()["id"]

def test_crear_plan_venta(client):
    response = client.post("/planes-venta/", json={
        "periodo": "mensual",
        "vendedor_id": vendedor_id,
        "producto_id": producto_id,  # ahora UUID
        "cuota": 100
    })
    assert response.status_code == 200
    assert response.json()["cuota"] == 100
    global plan_venta_id
    plan_venta_id = response.json()["id"]

def test_listar_planes_venta(client):
    response = client.get("/planes-venta/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_plan_venta(client):
    response = client.get(f"/planes-venta/{plan_venta_id}")
    assert response.status_code == 200
    assert response.json()["id"] == plan_venta_id

def test_eliminar_plan_venta(client):
    response = client.delete(f"/planes-venta/{plan_venta_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Plan de venta eliminado"
