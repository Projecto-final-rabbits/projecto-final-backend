# src/infrastructure/messaging/pubsub.py

import os
import json
import threading
from dotenv import load_dotenv
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from src.domain.events.event_type import EventType

# Carga variables de entorno
load_dotenv("src/.env")


class PubSubPublisher:
    """Publicador de eventos a Pub/Sub: productos → bodega, pedidos → pedidos_topic."""

    def __init__(self):
        creds_path = os.getenv("GCP_PUBSUB_CREDENTIALS_PATH")
        if not creds_path:
            raise RuntimeError("GCP_PUBSUB_CREDENTIALS_PATH no está definido")
        creds = service_account.Credentials.from_service_account_file(creds_path)

        self.publisher    = pubsub_v1.PublisherClient(credentials=creds)
        self.project_id   = os.getenv("CLOUD_PROJECT_ID")
        self.bodega_topic = os.getenv("PEDIDOS_BODEGA_TOPIC")
        self.pedido_topic = os.getenv("PEDIDO_TOPIC")

        if not all([self.project_id, self.bodega_topic, self.pedido_topic]):
            raise RuntimeError(
                "Faltan vars: CLOUD_PROJECT_ID, PEDIDOS_BODEGA_TOPIC o PEDIDO_TOPIC"
            )

    def publish_productos(self, productos: list[dict]):
        """
        Publica la lista de productos (con UUIDs) en PEDIDOS_BODEGA_TOPIC.
        """
        topic_path = self.publisher.topic_path(self.project_id, self.bodega_topic)
        data = json.dumps({"productos": productos}, default=str).encode("utf-8")
        self.publisher.publish(
            topic_path,
            data,
            event_type=EventType.bodega_product_list.value
        )
        print(f"✅ Publicado productos en topic '{self.bodega_topic}'")

    def publish_pedido(self, pedido: dict):
        """
        Publica el pedido completo en PEDIDO_TOPIC.
        """
        topic_path = self.publisher.topic_path(self.project_id, self.pedido_topic)
        data = json.dumps(pedido, default=str).encode("utf-8")
        self.publisher.publish(
            topic_path,
            data,
            event_type=EventType.pedido_created.value
        )
        print(f"✅ Publicado pedido en topic '{self.pedido_topic}'")


class PubSubSubscriber:
    """Suscriptor a Pub/Sub para recibir mensajes de PRODUCT_VENTAS_SUB."""

    def __init__(self):
        creds_path = os.getenv("GCP_PUBSUB_CREDENTIALS_PATH")
        if not creds_path:
            raise RuntimeError("GCP_PUBSUB_CREDENTIALS_PATH no está definido")
        creds = service_account.Credentials.from_service_account_file(creds_path)

        self.subscriber       = pubsub_v1.SubscriberClient(credentials=creds)
        self.project_id       = os.getenv("CLOUD_PROJECT_ID")
        self.product_sub      = os.getenv("PRODUCT_VENTAS_SUB")

        if not all([self.project_id, self.product_sub]):
            raise RuntimeError(
                "Faltan vars: CLOUD_PROJECT_ID o PRODUCT_VENTAS_SUB"
            )

    def subscribe_to_productos(self, callback: callable, daemon: bool = True):
        """
        Se suscribe a la subscription PRODUCT_VENTAS_SUB
        y delega cada mensaje JSON al callback.
        """
        sub_path = self.subscriber.subscription_path(
            self.project_id,
            self.product_sub
        )

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
