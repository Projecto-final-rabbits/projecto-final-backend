def test_crear_cliente(client):
    response = client.post("/clientes/", json={
        "nombre": "Luz Ruiz",
        "tipo_cliente": "mayorista",
        "direccion": "Calle Falsa 123",
        "telefono": "1234567890",
        "email": "Luz@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Luz Ruiz"
    assert data["email"] == "Luz@example.com"

def test_listar_clientes(client):
    response = client.get("/clientes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(c["nombre"] == "Luz Ruiz" for c in data)

def test_obtener_cliente(client):
    response = client.get("/clientes/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_cliente_no_existente(client):
    response = client.get("/clientes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"

def test_eliminar_cliente(client):
    response = client.delete("/clientes/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Cliente eliminado"
