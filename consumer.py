import kombu
import settings

from message_consumer import TaskConsumer

def main():
    with kombu.Connection(settings.RABBITMQ_DSN) as conn:
        consumer = TaskConsumer(conn)
        consumer.run()


if __name__ == "__main__":
    main()
