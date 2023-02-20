import logging
from typing import Any, Type

import kombu
from kombu.mixins import ConsumerMixin

import settings

MAX_RESEND = 3

log = logging.getLogger("plutus-dead-letter-consumer")


class DeadLetterConsumer(ConsumerMixin):
    dead_letter_queue = kombu.Queue(settings.DEAD_LETTER_QUEUE)

    def __init__(self, connection: kombu.Connection) -> None:
        self.connection = connection

    def get_consumers(self, Consumer: Type[kombu.Consumer], channel: Any) -> list[kombu.Consumer]:  # pragma: no cover
        return [Consumer(queues=[self.dead_letter_queue], callbacks=[self.on_message])]

    def on_message(self, body: dict, message: kombu.Message) -> None:  # pragma: no cover
        headers = message.headers
        resend_count = headers["x-death"][0]["count"]
        if resend_count > MAX_RESEND:
            log.debug(
                f"Message for transaction {body['transaction_id']} not delivered to data warehouse "
                f"after {MAX_RESEND} attempts."
            )
            message.reject()
        else:
            delay = 300 * resend_count
            log.debug(
                f"Resending message for transaction {body['transaction_id']} to data warehouse. "
                f"Next attempt {resend_count} in {delay/60} minutes"
            )
            producer = self.connection.Producer(serializer="json")
            producer.publish(
                body, headers=message.headers, routing_key=settings.DW_QUEUE_NAME, properties={"x-delay": delay}
            )


def main():
    with kombu.Connection(settings.RABBITMQ_DSN) as conn:
        consumer = DeadLetterConsumer(conn)
        consumer.run()


if __name__ == "__main__":
    main()
