import kombu
import settings

from plutus.message_consumer import MessageConsumer


def main():
    with kombu.Connection(settings.RABBITMQ_DSN) as conn:
        consumer = MessageConsumer(conn)
        consumer.run()


if __name__ == "__main__":
    main()
