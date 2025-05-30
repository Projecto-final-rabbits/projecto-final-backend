# import sys
# import pytest
# from unittest.mock import MagicMock
# from fastapi.testclient import TestClient
# import httpx

# # ✅ Mockear el módulo pubsub.py completo ANTES de cualquier import
# sys.modules["src.infrastructure.messaging.pubsub"] = MagicMock()

# from src.api.main import app
# from tests.db.test_database import TestingSessionLocal, init_test_db

# from src.api.routes import (
#     clientes_routes,
#     vendedores_routes,
#     productos_routes,
#     pedidos_routes,
#     detalles_routes,
#     planes_venta_routes,
# )

# @pytest.fixture(scope="session", autouse=True)
# def setup_test_database():
#     init_test_db()

# @pytest.fixture()
# def client():
#     def override_get_db():
#         db = TestingSessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()

#     # Overriding la base de datos en todos los routers
#     app.dependency_overrides[productos_routes.get_db] = override_get_db
#     app.dependency_overrides[clientes_routes.get_db] = override_get_db
#     app.dependency_overrides[vendedores_routes.get_db] = override_get_db
#     app.dependency_overrides[pedidos_routes.get_db] = override_get_db
#     app.dependency_overrides[detalles_routes.get_db] = override_get_db
#     app.dependency_overrides[planes_venta_routes.get_db] = override_get_db

#     return TestClient(app)

import sys
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import httpx

# ✅ Mockear pubsub completo ANTES de cualquier import
sys.modules["src.infrastructure.messaging.pubsub"] = MagicMock()

from src.api.main import app
from tests.db.test_database import TestingSessionLocal, init_test_db

from src.api.routes import (
    clientes_routes,
    vendedores_routes,
    productos_routes,
    pedidos_routes,
    detalles_routes,
    planes_venta_routes,
)

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

    # Override todas las rutas necesarias
    app.dependency_overrides[productos_routes.get_db] = override_get_db
    app.dependency_overrides[clientes_routes.get_db] = override_get_db
    app.dependency_overrides[vendedores_routes.get_db] = override_get_db
    app.dependency_overrides[pedidos_routes.get_db] = override_get_db
    app.dependency_overrides[detalles_routes.get_db] = override_get_db
    app.dependency_overrides[planes_venta_routes.get_db] = override_get_db

    return TestClient(app)

