from src.application.ports.out.event_publisher import EventPublisher
from src.infrastructure.messaging import pubsub
from src.domain.events.event_type import EventType

class PubsubEventPublisher(EventPublisher):
    def publish(self, event_type: EventType, data: dict):
        pubsub.publish_message(event_type, data)
