# tests/test_clientes_endpoints.py
import pytest

class TestClientesEndpoints:
    def test_crear_cliente(self, test_client):
        data = {
            "nombre": "Juan",
            "tipo_cliente": "VIP",
            "email": "juan@example.com",
            "telefono": "123456789",
            "fecha_registro": "2025-04-04"
        }
        response = test_client.post("/clientes/", json=data)
        assert response.status_code == 200, response.text
        json_data = response.json()
        assert json_data["nombre"] == "Juan"
        assert json_data["tipo_cliente"] == "VIP"

    def test_listar_clientes(self, test_client):
        # Asumimos que ya existen algunos clientes creados en tests anteriores
        response = test_client.get("/clientes/")
        assert response.status_code == 200, response.text
        clientes = response.json()
        assert isinstance(clientes, list)
        # Verificar que se encuentre al menos un cliente con nombre "Juan"
        assert any(cliente["nombre"] == "Juan" for cliente in clientes)

    def test_obtener_cliente(self, test_client):
        # Crear un cliente y luego obtenerlo por id
        data = {
            "nombre": "Carlos",
            "tipo_cliente": "Regular",
            "email": "carlos@example.com",
            "telefono": "999999",
            "fecha_registro": "2025-04-05"
        }
        create_response = test_client.post("/clientes/", json=data)
        assert create_response.status_code == 200, create_response.text
        client_id = create_response.json()["id"]

        get_response = test_client.get(f"/clientes/{client_id}")
        assert get_response.status_code == 200, get_response.text
        json_data = get_response.json()
        assert json_data["nombre"] == "Carlos"

    def test_eliminar_cliente(self, test_client):
        # Crear un cliente y luego eliminarlo
        data = {
            "nombre": "Luis",
            "tipo_cliente": "Regular",
            "email": "luis@example.com",
            "telefono": "888888",
            "fecha_registro": "2025-04-06"
        }
        create_response = test_client.post("/clientes/", json=data)
        assert create_response.status_code == 200, create_response.text
        client_id = create_response.json()["id"]

        delete_response = test_client.delete(f"/clientes/{client_id}")
        assert delete_response.status_code == 200, delete_response.text

        # Verificar que el cliente ya no exista
        get_response = test_client.get(f"/clientes/{client_id}")
        assert get_response.status_code == 404
