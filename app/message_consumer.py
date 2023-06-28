from typing import Any, Type

import kombu
import redis
from kombu.mixins import ConsumerMixin

import settings
from app.export_transaction import export_transaction_request_event, export_transaction_response_event


class MessageConsumer(ConsumerMixin):
    harmonia_audit_queue = kombu.Queue(settings.CONSUME_QUEUE_NAME)
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    def __init__(self, connection: kombu.Connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer: Type[kombu.Consumer], channel: Any) -> list[kombu.Consumer]:  # pragma: no cover
        return [Consumer(queues=[self.harmonia_audit_queue], callbacks=[self.on_message])]

    def on_message(self, body: dict, message: kombu.Message) -> None:  # pragma: no cover
        try:
            export_transaction_request_event(data=body, connection=self.connection, redis=self.r)
            export_transaction_response_event(data=body, connection=self.connection)
        finally:
            message.ack()


def main():
    with kombu.Connection(settings.RABBITMQ_DSN) as conn:
        consumer = MessageConsumer(conn)
        consumer.run()


if __name__ == "__main__":
    main()
