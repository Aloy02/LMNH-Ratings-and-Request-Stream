"""Kafka consumer for kiosk data."""

import json
from os import environ

from dotenv import load_dotenv
from confluent_kafka import Consumer
from confluent_kafka.cimpl import Message
from logger import setup_logger
from validate import is_valid
from datetime import datetime
from transform import transform
from load import load

logger = setup_logger()

TOPIC = 'lmnh'
TIMEOUT = 1.0


def is_valid_message(msg: Message) -> bool:
    """Check if the Kafka message is valid."""
    if msg is None:
        return False
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        return False
    return True


def decode_message(msg: Message) -> str:
    """Decode the Kafka message value to a UTF-8 string."""
    message = msg.value().decode('utf-8')
    kiosk_data = json.loads(message)
    if "at" not in kiosk_data:
        logger.info(f"Creating required key: 'at' in {kiosk_data}")
        kiosk_data["at"] = datetime.now().isoformat()

    return kiosk_data


def consume_message(cons: Consumer) -> dict:
    """Consume messages from the Kafka topic and push them the AWS RDS database."""
    cons.subscribe([TOPIC])
    while True:
        msg = cons.poll(TIMEOUT)

        if not is_valid_message(msg):
            continue

        kiosk_data = decode_message(msg)

        yield kiosk_data


if __name__ == "__main__":

    load_dotenv()

    conf = {
        'bootstrap.servers': environ["BOOTSTRAP_SERVERS"],
        'security.protocol': environ["SECURITY_PROTOCOL"],
        'sasl.mechanisms': environ["SASL_MECHANISM"],
        'sasl.username': environ["USERNAME"],
        'sasl.password': environ["PASSWORD"],
        'group.id': 'c26-aloysius-lmnh-consumer-update',
        'auto.offset.reset': 'earliest',
        "enable.auto.commit": False
    }

    with Consumer(conf) as consumer:
        for kiosk_data in consume_message(consumer):
            if not is_valid(kiosk_data):
                continue

            transformed_data = transform(kiosk_data)

            if transformed_data is None:
                logger.warning(
                    f"Transformed data is None for kiosk data: {kiosk_data}")
                continue

            load(transformed_data, consumer)
