import logging

from kombu import Connection, Exchange

log = logging.getLogger(__name__)


def _on_error(exc, interval):  # pragma: no cover
    log.warning(f"Failed to connect to RabbitMQ: {exc}. Will retry after {interval:.1f}s...")


def add(message: dict, provider: str, queue_name: str, connection: Connection) -> None:  # pragma: no cover
    connection.ensure_connection(
        errback=_on_error, max_retries=3, interval_start=0.2, interval_step=0.4, interval_max=1, timeout=3
    )
    q = connection.SimpleQueue(queue_name)
    q.put(message, headers={"X-Provider": provider})


def publish_to_exchange(message: dict, exchange: Exchange, queues: list, connection: Connection, headers={}) -> None:
    connection.ensure_connection(
        errback=_on_error, max_retries=3, interval_start=0.2, interval_step=0.4, interval_max=1, timeout=3
    )
    producer = connection.Producer(serializer="json")
    producer.publish(
        message, exchange=exchange, headers=headers, declare=queues
    )

