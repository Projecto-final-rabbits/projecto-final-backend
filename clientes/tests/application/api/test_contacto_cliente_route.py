from tests.conftest import create_cliente

class TestContactosEndpoints:
    def test_crear_contacto(self, test_client):
        cliente_id = create_cliente(test_client)
        data = {
            "cliente_id": cliente_id,  # Este campo debe ser aceptado por el schema de creación
            "nombre_contacto": "Carlos",
            "telefono": "123456",
            "email": "carlos@example.com"
        }
        response = test_client.post("/contactos/", json=data)
        assert response.status_code == 200, response.text
        json_data = response.json()
        # Se espera que se devuelva el campo cliente_id
        assert json_data["cliente_id"] == cliente_id
        assert json_data["nombre_contacto"] == "Carlos"

    # def test_listar_contactos(self, test_client):
    #     cliente_id = create_cliente(test_client)
    #     data1 = {
    #         "cliente_id": cliente_id,
    #         "nombre_contacto": "Carlos",
    #         "telefono": "123456",
    #         "email": "carlos@example.com"
    #     }
    #     data2 = {
    #         "cliente_id": cliente_id,
    #         "nombre_contacto": "Maria",
    #         "telefono": "654321",
    #         "email": "maria@example.com"
    #     }
    #     test_client.post("/contactos/", json=data1)
    #     test_client.post("/contactos/", json=data2)
    #     response = test_client.get("/contactos/")
    #     assert response.status_code == 200, response.text
    #     contactos = response.json()
    #     nombres = sorted([c["nombre_contacto"] for c in contactos])
    #     assert nombres == ["Carlos", "Maria"]

    def test_obtener_contacto(self, test_client):
        cliente_id = create_cliente(test_client)
        data = {
            "cliente_id": cliente_id,
            "nombre_contacto": "Luis",
            "telefono": "111222",
            "email": "luis@example.com"
        }
        create_response = test_client.post("/contactos/", json=data)
        contacto_id = create_response.json()["id"]
        get_response = test_client.get(f"/contactos/{contacto_id}")
        assert get_response.status_code == 200, get_response.text
        json_data = get_response.json()
        assert json_data["nombre_contacto"] == "Luis"

    def test_eliminar_contacto(self, test_client):
        cliente_id = create_cliente(test_client)
        data = {
            "cliente_id": cliente_id,
            "nombre_contacto": "Elena",
            "telefono": "333444",
            "email": "elena@example.com"
        }
        create_response = test_client.post("/contactos/", json=data)
        contacto_id = create_response.json()["id"]
        delete_response = test_client.delete(f"/contactos/{contacto_id}")
        assert delete_response.status_code == 200, delete_response.text
        get_response = test_client.get(f"/contactos/{contacto_id}")
        assert get_response.status_code == 404
