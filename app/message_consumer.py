from typing import Any, Type, cast

import kombu
from kombu.mixins import ConsumerMixin
from app.message_queue import publish_to_exchange

import settings

from .export_transaction import export_transaction_request_event, export_transaction_response_event


class MessageConsumer(ConsumerMixin):
    harmonia_audit_queue = kombu.Queue(settings.CONSUME_QUEUE_NAME)
    exchange = kombu.Exchange(settings.DEAD_LETTER_EXCHANGE, type="fanout")
    dead_letter_queue = kombu.Queue(settings.DEAD_LETTER_QUEUE, exchange=exchange)

    def __init__(self, connection: kombu.Connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer: Type[kombu.Consumer], channel: Any) -> list[kombu.Consumer]:  # pragma: no cover
        return [Consumer(queues=[self.harmonia_audit_queue], callbacks=[self.on_message])]

    def on_message(self, body: dict, message: kombu.Message) -> None:  # pragma: no cover
        try:
            if body["retry_count"] == 0:
                export_transaction_request_event(data=body, connection=self.connection)
            export_transaction_response_event(data=body, connection=self.connection)
        except (AttributeError, KeyError):
            publish_to_exchange(
                message=body,
                exchange=self.exchange,
                queues=[self.dead_letter_queue],
                connection=self.connection,
                headers=message.headers,
            )
        finally:
            message.ack()
