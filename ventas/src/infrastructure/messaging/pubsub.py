# src/infrastructure/messaging/pubsub.py

import os
import json
import threading
from dotenv import load_dotenv
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from src.domain.events.event_type import EventType

# Cargar variables de entorno
load_dotenv("src/.env")


def build_credentials():
    """Construye las credenciales de GCP dinámicamente."""
    environment = os.getenv("ENVIRONMENT", "local")  # por defecto 'production'
    
    if environment == "local":
        creds_path = os.getenv("GCP_PUBSUB_CREDENTIALS_PATH")
        if not creds_path:
            raise RuntimeError("GCP_PUBSUB_CREDENTIALS_PATH no está definido en local")
        return service_account.Credentials.from_service_account_file(creds_path)

    elif environment == "production":
        json_str = os.getenv("cloud-key-json")
        if json_str:
            service_account_info = json.loads(json_str)
            return service_account.Credentials.from_service_account_info(service_account_info)
        else:
            # Si no hay cloud-key-json, asumimos que GCP maneja las credenciales (Workload Identity)
            return None
    else:
        raise RuntimeError(f"ENVIRONMENT inválido: {environment}")


class PubSubPublisher:
    """Publicador de eventos a Pub/Sub."""

    def __init__(self):
        credentials = build_credentials()
        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        
        self.project_id = os.getenv("CLOUD_PROJECT_ID")
        self.bodega_topic = os.getenv("PEDIDOS_BODEGA_TOPIC")
        self.pedido_topic = os.getenv("PEDIDO_TOPIC")

        if not all([self.project_id, self.bodega_topic, self.pedido_topic]):
            raise RuntimeError("Faltan variables de entorno para PubSub")

    def publish_productos(self, productos: list[dict]):
        topic_path = self.publisher.topic_path(self.project_id, self.bodega_topic)
        data = json.dumps({"productos": productos}, default=str).encode("utf-8")
        self.publisher.publish(
            topic_path,
            data,
            event_type=EventType.bodega_product_list.value
        )
        print(f"✅ Publicado productos en topic '{self.bodega_topic}'")

    def publish_pedido(self, pedido: dict):
        topic_path = self.publisher.topic_path(self.project_id, self.pedido_topic)
        data = json.dumps(pedido, default=str).encode("utf-8")
        self.publisher.publish(
            topic_path,
            data,
            event_type=EventType.pedido_created.value
        )
        print(f"✅ Publicado pedido en topic '{self.pedido_topic}'")


class PubSubSubscriber:
    """Suscriptor de eventos de Pub/Sub."""

    def __init__(self):
        credentials = build_credentials()
        self.subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

        self.project_id = os.getenv("CLOUD_PROJECT_ID")
        self.product_sub = os.getenv("PRODUCT_VENTAS_SUB")

        if not all([self.project_id, self.product_sub]):
            raise RuntimeError("Faltan variables de entorno para PubSub")

    def subscribe_to_productos(self, callback: callable, daemon: bool = True):
        sub_path = self.subscriber.subscription_path(self.project_id, self.product_sub)

        def _wrapper(msg: pubsub_v1.subscriber.message.Message):
            msg_id = getattr(msg, "message_id", "<unknown>")
            try:
                payload = json.loads(msg.data.decode("utf-8"))
                msg.payload = payload
                callback(msg)
            except json.JSONDecodeError as e:
                print(f"[{msg_id}] JSON inválido: {e}")
                return msg.nack()

        future = self.subscriber.subscribe(sub_path, callback=_wrapper)
        print(f"🔔 Suscrito a '{self.product_sub}'")
        if daemon:
            threading.Thread(target=future.result, daemon=True).start()
        else:
            future.result()

