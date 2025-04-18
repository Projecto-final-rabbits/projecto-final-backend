from src.application.ports.out.event_publisher import EventPublisher
from src.infrastructure.messaging import pubsub
from src.domain.events.event_type import EventType

class PubsubEventPublisher(EventPublisher):
    def publish(self, event_type: EventType, data: dict):
        try:
            pubsub.publish_message(event_type, data)
        except Exception as e:
            print(f"🚨 Error al publicar en Pub/Sub: {e}")
            raise
