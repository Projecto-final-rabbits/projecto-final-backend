proveedor_id = None
orden_id = None

def test_crear_proveedor_para_orden(client):
    global proveedor_id
    response = client.post("/proveedores/", json={
        "nombre": "Proveedor Orden",
        "pais": "Perú",
        "contacto": "Ana Torres",
        "telefono": "3109988776",
        "email": "proveedor_orden@test.com"
    })
    assert response.status_code == 200
    print("proveedor_id creado", proveedor_id)
    proveedor_id = response.json()["id"]

def test_crear_orden_con_proveedor_inexistente(client):
    response = client.post("/ordenes/", json={
        "proveedor_id": 9999,
        "estado": "pendiente",
        "total": 100000.0
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Proveedor no encontrado"


def test_crear_orden_compra(client):
    global orden_id
    print("proveedor_id en test orden compra", proveedor_id)
    response = client.post("/ordenes/", json={
        "proveedor_id": proveedor_id,
        "estado": "pendiente",
        "total": 100000.0
    })
    assert response.status_code == 200
    orden_id = response.json()["id"]

# def test_listar_ordenes(client):
#     response = client.get("/ordenes/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

def test_obtener_orden_por_id(client):
    response = client.get(f"/ordenes/{orden_id}")
    assert response.status_code == 200
    assert response.json()["id"] == orden_id

def test_eliminar_orden(client):
    response = client.delete(f"/ordenes/{orden_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Orden eliminada"

def test_eliminar_proveedor_limpieza(client):
    response = client.delete(f"/proveedores/{proveedor_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Proveedor eliminado"
