import sys
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from unittest.mock import patch
import httpx

# ✅ Mockear el módulo pubsub.py completo ANTES de que cualquier import lo ejecute
sys.modules["src.infrastructure.messaging.pubsub"] = MagicMock()

from src.api.main import app
from tests.db.test_database import TestingSessionLocal, init_test_db
from src.api.routes import productos_routes


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

    app.dependency_overrides[productos_routes.get_db] = override_get_db
    
    return TestClient(app)

@pytest.fixture(autouse=True)
def mock_proveedor_existe():
    with patch("src.application.services.proveedores_service.httpx.get") as mock_get:
        mock_get.return_value = httpx.Response(200)
        yield
