import os
import threading
import logging
import json
from typing import Callable

from google.cloud import pubsub_v1
from google.oauth2 import service_account

class PubSubVentasProductosSubscriber:
    """Escucha el sub `PEDIDOS_BODEGA_SUB` y delega al callback recibido."""

    _PROJECT_ID       = os.getenv("CLOUD_PROJECT_ID", "")
    _SUB_ID           = os.getenv("PEDIDOS_BODEGA_SUB", "pedidos_bodegas_sub")
    _CREDENTIALS_PATH = os.getenv("GCP_PUBSUB_CREDENTIALS_PATH", "src/cloud-key.json")

    def __init__(self, callback: Callable[[dict], None]) -> None:
        # Validar configuración
        if not all([self._PROJECT_ID, self._SUB_ID, self._CREDENTIALS_PATH]):
            raise RuntimeError(
                f"Configuración incompleta: "
                f"CLOUD_PROJECT_ID={self._PROJECT_ID!r}, "
                f"PEDIDOS_BODEGA_SUB={self._SUB_ID!r}, "
                f"GCP_PUBSUB_CREDENTIALS_PATH={self._CREDENTIALS_PATH!r}"
            )

        creds = service_account.Credentials.from_service_account_file(self._CREDENTIALS_PATH)
        self._subscriber = pubsub_v1.SubscriberClient(credentials=creds)
        self._sub_path   = self._subscriber.subscription_path(self._PROJECT_ID, self._SUB_ID)
        self._callback_domain = callback

    def start(self, daemon: bool = False) -> None:
        """Arranca el listener; bloquea o lanza hilo daemon según flag."""
        future = self._subscriber.subscribe(self._sub_path, callback=self._wrapper)
        logging.info(f"🛰️  Escuchando {self._SUB_ID} ...")
        if daemon:
            threading.Thread(target=self._run_future, args=(future,), daemon=True).start()
        else:
            self._run_future(future)

    def _run_future(self, future) -> None:
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
        finally:
            self._subscriber.close()

    def _wrapper(self, message: pubsub_v1.subscriber.message.Message) -> None:
        msg_id = getattr(message, "message_id", "<unknown>")
        # 1) Decodificar JSON
        try:
            payload = json.loads(message.data.decode("utf-8"))
        except json.JSONDecodeError as e:
            logging.error(f"[{msg_id}] JSON inválido: {e}")
            return message.nack()

        # 2) Delegar a la lógica de dominio
        try:
            self._callback_domain(payload)
            message.ack()
            logging.info(f"[{msg_id}] Procesado con éxito. ACK enviado.")
        except ValueError as err:
            logging.warning(f"[{msg_id}] Error de dominio: {err}")
            message.nack()
        except Exception:
            logging.exception(f"[{msg_id}] Error inesperado procesando mensaje:")
            message.nack()
