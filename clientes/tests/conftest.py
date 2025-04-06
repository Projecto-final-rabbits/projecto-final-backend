import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import Base, SessionLocal
from src.api.main import app  # Asegúrate de que esta ruta es correcta

# Configurar la base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas en la base de datos en memoria
Base.metadata.create_all(bind=engine)

# Override de la dependencia get_db para usar la sesión de testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[SessionLocal] = override_get_db

@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)

# Función helper para crear un cliente, la hacemos "global" en conftest para importarla en los tests
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
