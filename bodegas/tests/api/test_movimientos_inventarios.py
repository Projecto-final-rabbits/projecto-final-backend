
import pytest
from uuid import uuid4
from datetime import datetime

@pytest.fixture
def producto_id():
    return str(uuid4())

@pytest.fixture
def bodega(client):
    response = client.post("/bodegas/", json={
        "nombre": "Bodega Test",
        "ciudad": "Ciudad Test",
        "pais": "País Test",
        "direccion": "Dirección Test"
    })
    return response.json()["id"]

def test_registrar_entrada_producto(client, bodega, producto_id):
    movimiento = {
        "producto_id": producto_id,
        "bodega_id": bodega,
        "cantidad": 10,
        "tipo_movimiento": "entrada",
        "descripcion": "Ingreso inicial"
    }
    response = client.post("/movimientos/entrada", json=movimiento)
    print("Response obtenida en el test:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["producto_id"] == producto_id
    assert data["cantidad"] == 10
    assert data["tipo_movimiento"] == "entrada"

def test_listar_movimientos(client):
    response = client.get("/movimientos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_listar_inventarios(client):
    response = client.get("/inventarios/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
