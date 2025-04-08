import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import Base
from src.infrastructure.adapters.cliente_repository_sqlalchemy import ClienteRepositorySQLAlchemy
from src.application.schemas.clientes import ClienteCreate

# Configuración de la base de datos en memoria
@pytest.fixture(scope="module")
def db_session():
    # Crear una base de datos en memoria para pruebas
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()


# Crear el repositorio que se usará en las pruebas
@pytest.fixture
def cliente_repository(db_session):
    return ClienteRepositorySQLAlchemy()


# Prueba para crear un cliente
def test_crear_cliente(cliente_repository, db_session):
    cliente_data = ClienteCreate(nombre="Juan", tipo_cliente="VIP", email="juan@example.com", telefono="123456789", fecha_registro="2025-04-04")
    cliente = cliente_repository.guardar(db_session, cliente_data)
    assert cliente.id is not None
    assert cliente.nombre == "Juan"
    assert cliente.tipo_cliente == "VIP"
    assert cliente.email == "juan@example.com"


# Prueba para listar todos los clientes
def test_listar_clientes(cliente_repository, db_session):
    cliente_data1 = ClienteCreate(nombre="Juan", tipo_cliente="VIP", email="juan@example.com", telefono="123456789", fecha_registro="2025-04-04")
    cliente_data2 = ClienteCreate(nombre="Ana", tipo_cliente="Regular", email="ana@example.com", telefono="987654321", fecha_registro="2025-04-05")

    cliente_repository.guardar(db_session, cliente_data1)
    cliente_repository.guardar(db_session, cliente_data2)

    clientes = cliente_repository.listar_todos(db_session)

    assert clientes[1].nombre == "Juan"
    assert clientes[2].nombre == "Ana"


# Prueba para obtener un cliente por id
def test_obtener_cliente(cliente_repository, db_session):
    cliente_data = ClienteCreate(nombre="Juan", tipo_cliente="VIP", email="juan@example.com", telefono="123456789", fecha_registro="2025-04-04")
    cliente = cliente_repository.guardar(db_session, cliente_data)

    cliente_obtenido = cliente_repository.obtener_por_id(db_session, cliente.id)
    assert cliente_obtenido is not None
    assert cliente_obtenido.id == cliente.id
    assert cliente_obtenido.nombre == "Juan"


# Prueba para eliminar un cliente
def test_eliminar_cliente(cliente_repository, db_session):
    cliente_data = ClienteCreate(nombre="Juan", tipo_cliente="VIP", email="juan@example.com", telefono="123456789", fecha_registro="2025-04-04")
    cliente = cliente_repository.guardar(db_session, cliente_data)

    response = cliente_repository.eliminar(db_session, cliente.id)
    assert response["message"] == "Cliente eliminado"

    # Verificar que el cliente ha sido eliminado
    cliente_eliminado = cliente_repository.obtener_por_id(db_session, cliente.id)
    assert cliente_eliminado is None
