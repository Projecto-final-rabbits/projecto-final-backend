# src/infrastructure/messaging/pubsub.py

import os
import json
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from src.domain.events.event_type import EventType

class PubSubPublisher:
    def __init__(self):
        creds_path       = os.getenv("GCP_PUBSUB_CREDENTIALS_PATH")
        creds            = service_account.Credentials.from_service_account_file(creds_path)
        self.publisher   = pubsub_v1.PublisherClient(credentials=creds)
        self.project_id  = os.getenv("CLOUD_PROJECT_ID")
        self.pedido_topic= os.getenv("PEDIDO_TOPIC")
        self.bodega_topic= os.getenv("PEDIDOS_BODEGA_TOPIC")

    def publish_productos(self, productos: list[dict]):
        """
        Publica la lista de productos (con UUIDs) en PEDIDOS_BODEGA_TOPIC.
        """
        topic_path = self.publisher.topic_path(self.project_id, self.bodega_topic)
        # Usamos default=str para serializar UUIDs
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
        # default=str para serializar cualquier UUID o date
        data = json.dumps(pedido, default=str).encode("utf-8")
        self.publisher.publish(
            topic_path,
            data,
            event_type=EventType.pedido_created.value
        )
        print(f"✅ Publicado pedido en topic '{self.pedido_topic}'")
