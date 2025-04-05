import json
from src.config.database import SessionLocal
from src.infrastructure.adapters.producto_repository_sqlalchemy import ProductoRepositorySQLAlchemy
from src.application.services.productos_event_service import ProductoEventService

def handle_product_created(message):
    try:
        print("📩 Mensaje recibido en COMPRAS:", flush=True)
        data = json.loads(message.data.decode("utf-8"))
        print(f"🧾 Data: {data}", flush=True)

        db = SessionLocal()
        repo = ProductoRepositorySQLAlchemy()
        service = ProductoEventService(repo)
        creado = service.crear_producto_desde_evento(db, data)
        print(f"✅ Producto creado por evento: {creado.id}", flush=True)

        message.ack()
    except Exception as e:
        print(f"🚨 Error al procesar mensaje: {e}", flush=True)
        message.nack()