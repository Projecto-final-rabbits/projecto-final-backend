import sys
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from tests.db.test_database import TestingSessionLocal, init_test_db
from unittest.mock import MagicMock

sys.modules["src.infrastructure.messaging.pubsub"] = MagicMock()

from src.api.routes import proveedores_routes, productos_routes, ordenes_routes, detalles_routes

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    init_test_db()  

@pytest.fixture()
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[proveedores_routes.get_db] = override_get_db
    app.dependency_overrides[productos_routes.get_db] = override_get_db
    app.dependency_overrides[ordenes_routes.get_db] = override_get_db
    app.dependency_overrides[detalles_routes.get_db] = override_get_db

    return TestClient(app)
