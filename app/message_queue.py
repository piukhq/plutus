import logging

import kombu
from kombu import Connection, Exchange, Queue

import settings

log = logging.getLogger(__name__)


dl_exchange = Exchange(settings.DEAD_LETTER_EXCHANGE, type="fanout")
dw_queue = Queue(
    settings.DW_QUEUE_NAME,
    queue_arguments={
        "x-dead-letter-routing-key": settings.DEAD_LETTER_QUEUE,
        "x-dead-letter-exchange": settings.DEAD_LETTER_EXCHANGE,
    },
)
dead_letter_queue = kombu.Queue(settings.DEAD_LETTER_QUEUE, exchange=dl_exchange)


def _on_error(exc, interval):  # pragma: no cover
    log.warning(f"Failed to connect to RabbitMQ: {exc}. Will retry after {interval:.1f}s...")


def add(message: dict, connection: Connection) -> None:  # pragma: no cover
    connection.ensure_connection(
        errback=_on_error, max_retries=3, interval_start=0.2, interval_step=0.4, interval_max=1, timeout=3
    )
    producer = connection.Producer(serializer="json")
    producer.publish(
        message,
        routing_key=settings.DW_QUEUE_NAME,
        declare=[dl_exchange, dead_letter_queue, dw_queue],
    )
