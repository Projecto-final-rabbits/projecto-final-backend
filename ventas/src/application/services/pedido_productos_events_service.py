# src/infrastructure/adapters/out/pubsub_event_publisher.py
class PubsubEventPublisher:
    """Publica mensajes en Google Cloud Pub/Sub.

    Métodos reales omitidos; sólo la interfaz usada más abajo.
    """
    def publish(self, topic: str, message: dict) -> None:
        ...
