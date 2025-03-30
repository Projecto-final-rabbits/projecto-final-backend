proveedor_data = {
    "nombre": "Proveedor Test",
    "pais": "Colombia",
    "contacto": "Juan Pérez",
    "telefono": "3211234567",
    "email": "proveedor@test.com"
}

def test_crear_proveedor(client):
    response = client.post("/proveedores/", json=proveedor_data)
    assert response.status_code == 200
    assert response.json()["nombre"] == proveedor_data["nombre"]
    global proveedor_id
    proveedor_id = response.json()["id"]

def test_listar_proveedores(client):
    response = client.get("/proveedores/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obtener_proveedor_por_id(client):
    response = client.get(f"/proveedores/{proveedor_id}")
    assert response.status_code == 200
    assert response.json()["id"] == proveedor_id

def test_eliminar_proveedor(client):
    response = client.delete(f"/proveedores/{proveedor_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Proveedor eliminado"
