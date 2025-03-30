def test_crear_vendedor_y_producto_para_plan(client):
    # Vendedor
    response = client.post("/vendedores/", json={
        "nombre": "Vendedor Plan",
        "zona": "Occidente",
        "telefono": "3003003000",
        "email": "vendedor@plan.com"
    })
    assert response.status_code == 200

    # Producto
    response = client.post("/productos/", json={
        "nombre": "Monitor",
        "descripcion": "Monitor Full HD",
        "precio_venta": 800.0,
        "stock": 50,
        "categoria": "Pantallas"
    })
    assert response.status_code == 200

def test_crear_plan_venta(client):
    response = client.post("/planes-venta/", json={
        "periodo": "mensual",
        "vendedor_id": 2,
        "producto_id": 2,
        "cuota": 100
    })
    print(response.json(),"response.json()")
    assert response.status_code == 200
    assert response.json()["cuota"] == 100

def test_listar_planes_venta(client):
    response = client.get("/planes-venta/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_plan_venta(client):
    response = client.get("/planes-venta/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_eliminar_plan_venta(client):
    response = client.delete("/planes-venta/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Plan de venta eliminado"
