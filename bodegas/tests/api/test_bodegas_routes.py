def test_listar_bodegas_vacia(client):
    response = client.get("/bodegas/")
    assert response.status_code == 200
    assert response.json() == []

def test_crear_bodega(client):
    nueva_bodega = {
        "nombre": "Bodega Norte Bogotá",
        "direccion": "Autopista Norte #125-30",
        "ciudad": "Bogotá",
        "pais": "Colombia"
    }
    response = client.post("/bodegas/", json=nueva_bodega)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == nueva_bodega["nombre"]
    assert "id" in data
    client.bodega_id_creada = data["id"]

def test_obtener_bodega(client):
    response_crear = client.post("/bodegas/", json={
        "nombre": "Centro Logístico Guayaquil",
        "direccion": "Av. Juan Tanca Marengo, Km 5.5",
        "ciudad": "Guayaquil",
        "pais": "Ecuador"
    })
    bodega_id = response_crear.json()["id"]
    response = client.get(f"/bodegas/{bodega_id}")
    assert response.status_code == 200
    assert response.json()["id"] == bodega_id

def test_obtener_bodega_inexistente(client):
    response = client.get("/bodegas/999999")
    assert response.status_code == 404

def test_eliminar_bodega(client):
    response_crear = client.post("/bodegas/", json={
        "nombre": "Depósito San Miguel",
        "direccion": "Av. La Marina 740, San Miguel",
        "ciudad": "Lima",
        "pais": "Perú"
    })
    bodega_id = response_crear.json()["id"]
    response = client.delete(f"/bodegas/{bodega_id}")
    assert response.status_code == 204
    response_check = client.get(f"/bodegas/{bodega_id}")
    assert response_check.status_code == 404
