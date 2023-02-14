import os
import typing as t


class ConfigVarRequiredError(Exception):
    pass


def getenv(key: str, default: str = "", conv: t.Callable = str, required: bool = True) -> t.Any:
    """If `default` is None, then the var is non-optional."""
    var = os.getenv(key, default)
    if var is None and required is True:
        raise ConfigVarRequiredError(f"Configuration variable '{key}' is required but was not provided.")
    elif var is not None:
        return conv(var)
    else:
        return None


def boolconv(s: str) -> bool:
    return s.lower() in ["true", "t", "yes"]


RABBITMQ_USER = getenv("RABBITMQ_USER", required=True, default="guest")
RABBITMQ_PASS = getenv("RABBITMQ_PASS", required=True, default="guest")
RABBITMQ_HOST = getenv("RABBITMQ_HOST", required=True, default="localhost")
RABBITMQ_PORT = getenv("RABBITMQ_PORT", required=True, conv=int, default="5672")
RABBITMQ_DSN = getenv("AMQP_DSN", f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//")

CONSUME_QUEUE_NAME = getenv("CONSUME_QUEUE", required=True, default="tx_plutus_dw")
DW_QUEUE_NAME = getenv("DW_QUEUE", required=True, default="tx_export_dw")
DEAD_LETTER_EXCHANGE = getenv("DEAD_LETTER_EXCHANGE", required=True, default="tx_plutus_dl_exchange")
DEAD_LETTER_QUEUE = getenv("DEAD_LETTER_QUEUE", required=True, default="tx_plutus_dl_queue")
