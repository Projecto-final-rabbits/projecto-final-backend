from google.cloud import pubsub_v1
from google.oauth2 import service_account
import os
import threading
import json
from dotenv import load_dotenv

load_dotenv("src/.env")

from src.domain.events.event_type import EventType

json_str = os.getenv("cloud-key-json")
if not json_str:
    raise RuntimeError("GCP_PUBSUB_CREDENTIALS_PATH is not set")

service_account_info = json.loads(json_str)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

#credentials = service_account.Credentials.from_service_account_file("src/cloud-key.json")
publisher = pubsub_v1.PublisherClient(credentials=credentials)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

project_id = os.getenv("CLOUD_PROJECT_ID")
topic_id = os.getenv("PRODUCT_TOPIC")
subscription_id = os.getenv("PEDIDOS_BODEGA_SUB")


def publish_message(event_type: EventType, data: dict):
    project_id = os.getenv("CLOUD_PROJECT_ID")
    topic_id = os.getenv("PRODUCT_TOPIC")
    topic_path = publisher.topic_path(project_id, topic_id)

    data_str = json.dumps(data, default=str)
    try:
        future = publisher.publish(
            topic_path,
            data_str.encode("utf-8"),
            event_type="product-created"
        )
        future.result()
        print("✅ Mensaje publicado correctamente.")
    except Exception as e:
        print(f"🚨 Error al publicar en Pub/Sub: {e}")
        raise

def subscribe_to_topic(callback):
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    threading.Thread(target=streaming_pull_future.result).start()

