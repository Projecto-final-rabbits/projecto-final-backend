def test_crear_producto(client):
    global producto_id
    response = client.post("/productos/", json={
        "nombre": "Teclado",
        "descripcion": "Teclado mecánico",
        "precio_venta": 200.0,
        "categoria": "Periféricos",
        "promocion_activa": False
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Teclado"
    producto_id = response.json()["id"]

def test_listar_productos(client):
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(p["id"] == producto_id for p in response.json())

def test_obtener_producto(client):
    response = client.get(f"/productos/{producto_id}")
    assert response.status_code == 200
    assert response.json()["id"] == producto_id

def test_eliminar_producto(client):
    response = client.delete(f"/productos/{producto_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Producto eliminado"
