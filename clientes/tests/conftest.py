import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import Base, SessionLocal
from src.api.main import app  # Asegúrate de que esta ruta es correcta

# Validación de entorno para determinar la base de datos
if os.getenv("TESTING") == "true" or os.getenv("PYTEST_CURRENT_TEST"):
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    connect_args = {"check_same_thread": False}
else:
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
    connect_args = {}

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL no está definido")

# Configurar la base de datos con la URL y los connect_args determinados
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Override de la dependencia get_db para usar la sesión de testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Se sobreescribe la dependencia en la aplicación
app.dependency_overrides[SessionLocal] = override_get_db

@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)

# Función helper para crear un cliente, disponible para todos los tests.
def create_cliente(test_client, nombre="Test Cliente"):
    data = {
        "nombre": nombre,
        "tipo_cliente": "Test",
        "email": "testcliente@example.com",
        "telefono": "000000000",
        "fecha_registro": "2025-04-01"
    }
    response = test_client.post("/clientes/", json=data)
    assert response.status_code == 200, response.text
    return response.json()["id"]
