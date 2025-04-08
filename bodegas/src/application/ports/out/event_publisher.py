from abc import ABC, abstractmethod
from src.domain.events.event_type import EventType

class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event_type: EventType, data: dict):
        pass
