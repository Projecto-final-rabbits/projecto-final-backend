# src/infrastructure/handlers/pedido_created_handler.py
import json
from sqlalchemy.orm import Session
from src.config.database import SessionLocal
from src.infrastructure.adapters.pedido_repository_sqlalchemy import PedidoRepositorySQLAlchemy
from src.application.schemas.clientes import PedidoCreate

def pedido_created_handler(message):
    session: Session = SessionLocal()
    repo = PedidoRepositorySQLAlchemy()

    try:
        print("📩 Mensaje recibido (pedido_created)", flush=True)
        payload = json.loads(message.data.decode("utf-8"))
        print(f"🧾 Payload: {payload}", flush=True)

        # Extraemos sólo los campos que necesitamos
        data = {
            "cliente_id": payload["cliente_id"],
            "vendedor_id": payload["vendedor_id"],
            "fecha_envio": payload["fecha_envio"],
            "direccion_entrega": payload["direccion_entrega"],
            "estado": payload.get("estado", "pendiente"),
        }
        pedido_in = PedidoCreate(**data)

        nuevo = repo.guardar(session, pedido_in)
        print(f"✅ Pedido {nuevo.id} guardado para cliente {nuevo.cliente_id}", flush=True)

        session.commit()
        message.ack()
        print("🔔 Mensaje ack()", flush=True)

    except Exception as e:
        session.rollback()
        print(f"🚨 Error en pedido_created_handler: {e}", flush=True)
        message.nack()
        print("🔄 Mensaje nack()", flush=True)

    finally:
        session.close()
        print("🔒 Sesión DB cerrada", flush=True)

