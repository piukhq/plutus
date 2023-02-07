from typing import Any, Type

import kombu
from kombu.mixins import ConsumerMixin

import settings

from .export_transaction import (export_transaction_request_event,
                                 export_transaction_response_event)


class MessageConsumer(ConsumerMixin):
    harmonia_audit_queue = kombu.Queue(settings.CONSUME_QUEUE_NAME)

    def __init__(self, connection: kombu.Connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer: Type[kombu.Consumer], channel: Any) -> list[kombu.Consumer]:
        return [Consumer(queues=[self.harmonia_audit_queue], callbacks=[self.on_message])]

    @staticmethod
    def on_message(body: dict, message: kombu.Message) -> None:  # pragma: no cover
        try:
            if body["retry_count"] == 0:
                export_transaction_request_event(data=body)
            export_transaction_response_event(data=body)
        finally:
            message.ack()
