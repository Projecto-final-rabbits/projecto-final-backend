from google.cloud import pubsub_v1
from google.oauth2 import service_account
import os
import threading
import json
from dotenv import load_dotenv

load_dotenv("src/.env")

json_str = os.getenv("cloud-key-json")
if not json_str:
    raise RuntimeError("GCP_PUBSUB_CREDENTIALS_PATH is not set")

service_account_info = json.loads(json_str)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# credentials = service_account.Credentials.from_service_account_file("src/cloud-key.json")
publisher = pubsub_v1.PublisherClient(credentials=credentials)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

project_id = os.getenv("CLOUD_PROJECT_ID")
subscription_id = os.getenv("PEDIDO_SUB")


def subscribe_to_topic(callback):
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    threading.Thread(target=streaming_pull_future.result).start()
