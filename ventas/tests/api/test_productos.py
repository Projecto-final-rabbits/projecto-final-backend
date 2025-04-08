def test_crear_producto(client):
    response = client.post("/productos/", json={
        "nombre": "Teclado",
        "descripcion": "Teclado mecánico",
        "precio_venta": 200.0,
        "categoria": "Periféricos"
    })
    assert response.status_code == 200
    assert response.json()["nombre"] == "Teclado"

def test_listar_productos(client):
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(p["nombre"] == "Teclado" for p in response.json())

def test_obtener_producto(client):
    response = client.get("/productos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_eliminar_producto(client):
    response = client.delete("/productos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Producto eliminado"
