from uuid import UUID

proveedor_id = None
producto_id: UUID | None = None

def test_crear_proveedor_para_producto(client):
    global proveedor_id
    response = client.post("/proveedores/", json={
        "nombre": "Proveedor Producto",
        "pais": "México",
        "contacto": "Carlos Ruiz",
        "telefono": "3129876543",
        "email": "proveedor_producto@test.com"
    })
    assert response.status_code == 200
    proveedor_id = response.json()["id"]

def test_crear_producto_con_proveedor_inexistente(client):
    response = client.post("/productos/", json={
        "nombre": "Producto inválido",
        "descripcion": "Proveedor no existe",
        "precio_compra": 20000.0,
        "categoria": "Otros",
        "tiempo_entrega_dias": 2,
        "proveedor_id": 9999 
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Proveedor no encontrado"

def test_crear_producto(client):
    global producto_id
    response = client.post("/productos/", json={
        "nombre": "Producto de prueba",
        "descripcion": "Producto de prueba para test",
        "precio_compra": 15000.0,
        "categoria": "Tecnología",
        "tiempo_entrega_dias": 3,
        "proveedor_id": proveedor_id
    })
    assert response.status_code == 200
    producto_id = response.json()["id"]

def test_listar_productos(client):
    response = client.get("/productos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filtrar_productos_por_pais(client):
    response = client.get("/productos/", params={"pais": "México"})
    assert response.status_code == 200
    productos = response.json()
    assert isinstance(productos, list)
    assert len(productos) >= 1
    for producto in productos:
        assert producto["proveedor_id"] == proveedor_id

def test_obtener_producto_por_id(client):
    response = client.get(f"/productos/{producto_id}")
    assert response.status_code == 200
    assert response.json()["id"] == producto_id

def test_eliminar_producto(client):
    response = client.delete(f"/productos/{producto_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Producto eliminado"

def test_eliminar_proveedor_limpieza(client):
    response = client.delete(f"/proveedores/{proveedor_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Proveedor eliminado"
