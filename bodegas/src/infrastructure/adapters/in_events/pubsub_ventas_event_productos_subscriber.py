# src/infrastructure/handlers/ventas_productos_handler.py
import json
from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.infrastructure.adapters.inventario_repository_sqlalchemy import InventarioRepository

def ventas_productos_handler(message):
    """
    Handler que procesa el evento 'pedido_created' desde Pub/Sub.
    Por cada producto en el pedido, descuenta la cantidad del inventario.
    """
    session: Session = SessionLocal()
    repo = InventarioRepository(session)

    try:
        print("📩 Mensaje recibido en Bodega de pedido creado:", flush=True)
        payload = json.loads(message.data.decode("utf-8"))
        print(f"🧾 Payload: {payload}", flush=True)

        productos: list[dict] = payload.get("productos", [])
        if not productos:
            raise ValueError("El payload no incluye la lista 'productos'")

        # 1) Descontar stock de cada producto
        for item in productos:
            prod_id = item.get("producto_id")
            cantidad = item.get("cantidad", 0)

            if not prod_id:
                raise ValueError(f"Falta 'producto_id' en item: {item}")
            if cantidad <= 0:
                raise ValueError(f"Cantidad inválida ({cantidad}) para producto {prod_id}")

            repo.descontar_stock(prod_id, cantidad)
            print(f"✅ Descontado {cantidad} unidades de inventario para producto {prod_id}", flush=True)

        # 2) Confirmar cambios en BD
        session.commit()
        print("✅ Inventario actualizado con éxito", flush=True)

        # 3) Confirmar procesamiento del mensaje
        message.ack()
        print("🔔 Mensaje ack() enviado a Pub/Sub", flush=True)

    except Exception as e:
        session.rollback()
        print(f"🚨 Error al procesar mensaje de ventas_productos_handler: {e}", flush=True)
        message.nack()
        print("🔄 Mensaje nack() enviado a Pub/Sub", flush=True)

    finally:
        session.close()
        print("🔒 Sesión de DB cerrada", flush=True)
