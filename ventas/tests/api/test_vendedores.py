def test_crear_vendedor(client):
    response = client.post("/vendedores/", json={
        "nombre": "Laura Vendedora",
        "zona": "Norte",
        "telefono": "123456789",
        "email": "laura@ventas.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Laura Vendedora"
    assert data["zona"] == "Norte"

def test_listar_vendedores(client):
    response = client.get("/vendedores/")
    assert response.status_code == 200
    vendedores = response.json()
    assert isinstance(vendedores, list)
    assert any(v["nombre"] == "Laura Vendedora" for v in vendedores)

def test_obtener_vendedor(client):
    response = client.get("/vendedores/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["nombre"] == "Vendedor Detalle"

def test_eliminar_vendedor(client):
    response = client.delete("/vendedores/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Vendedor eliminado"

def test_obtener_vendedor_inexistente(client):
    response = client.get("/vendedores/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Vendedor no encontrado"
