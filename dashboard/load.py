"""Module for loading data into the AWS RDS."""
from datetime import datetime

import psycopg2
from psycopg2.extensions import connection
from psycopg2 import sql
from psycopg2.extras import execute_values

from os import environ
from dotenv import load_dotenv

from logger import setup_logger
import json

logger = setup_logger()


def insert_ratings(batch: list[dict]):
    """Insert multiple ratings into the database."""
    conn = get_conn()
    query = sql.SQL(
        """
    INSERT INTO ratings
    (exhibition_id, rating_value, time_at)
    VALUES %s;
    """)

    template = "(%(exhibition_id)s, %(rating_value)s, %(time_at)s)"

    with conn.cursor() as cursor:
        execute_values(cursor, query, batch, template=template)
        logger.info(
            f"Successfully inserted {len(batch)} ratings into database.")

    conn.commit()

    conn.close()


def insert_request(packet: dict):
    """Insert a single request into the database."""
    logger.info(
        f"Processing request event for exhibition {packet.get('exhibition_id')}.")
    conn = get_conn()
    query = sql.SQL(
        """
    INSERT INTO requests
    (exhibition_id, request_value, time_at)
    VALUES (%(exhibition_id)s, %(request_value)s, %(time_at)s);
    """)
    with conn.cursor() as cursor:
        cursor.execute(query, packet)
        logger.info(
            f"Successfully inserted request for exhibition {packet.get('exhibition_id')}.")

    conn.commit()
    conn.close()


def get_conn() -> connection:
    """Get a connection to the AWS RDS."""
    try:
        conn = psycopg2.connect(
            dbname=environ.get("DB_NAME"),
            user=environ.get("DB_USER"),
            password=environ.get("DB_PASSWORD"),
            host=environ.get("DB_HOST"),
            port=environ.get("DB_PORT")
        )
        logger.debug(f"Connected to database: {environ.get('DB_HOST')}")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Failed to connect to database: {e}")
        raise


class RatingQueue:
    def __init__(self, threshold: int = 10):
        """Initialise the rating queue."""
        self._queue = []
        self._threshold = threshold

        self.load()

    def queue(self, packet: dict):
        """Add a rating to the queue and process if the queue reaches the threshold."""
        self._queue.append(packet)
        queue_size = len(self._queue)
        if queue_size >= self._threshold:
            logger.info(
                f"Queue threshold reached ({queue_size}/{self._threshold}). Flushing ratings.")
            batch = self._queue.copy()
            insert_ratings(batch)
            self._queue.clear()
        else:
            logger.debug(
                f"Rating queued. Queue size: {queue_size}/{self._threshold}")
        self.save()

    def save(self):
        """Save the current queue in a JSON file."""
        logger.info(
            f"Saving remaining ratings in queue ({len(self._queue)}/{self._threshold}) to JSON file.")
        with open("rating_queue.json", "w", encoding="utf-8") as f:
            json.dump(self._queue, f)

    def load(self):
        """Load the queue from a JSON file."""
        try:
            with open("rating_queue.json", "r", encoding="utf-8") as f:
                self._queue = json.load(f)
            logger.info(
                f"Loaded {len(self._queue)} ratings from JSON file into the queue.")
        except FileNotFoundError:
            logger.debug("No JSON file found. Starting with an empty queue.")
            with open("rating_queue.json", "w+", encoding="utf-8") as f:
                json.dump([], f)


rating_queue = RatingQueue()


def queue_rating(packet: dict):
    """Queue a rating for further processing."""
    logger.debug(
        f"Queuing rating for exhibition {packet.get('exhibition_id')}.")
    rating_queue.queue(packet)


def load(kiosk_datagram: dict, consumer) -> None:
    """Load data into the AWS RDS."""

    kiosk_data = kiosk_datagram.get("payload")

    event_type = kiosk_datagram.get("event_type")

    if event_type is None:
        logger.error("Event type is None. Skipping load.")
        return

    if event_type == "rating":
        try:
            queue_rating(kiosk_data)
            consumer.commit()
        except Exception as e:
            logger.error(f"Failed to queue rating: {e}")

    elif event_type == "request":
        try:
            insert_request(kiosk_data)
            consumer.commit()
        except Exception as e:
            logger.error(f"Failed to insert request: {e}")
    else:
        logger.warning(f"Unknown event type: {event_type}. Skipping load.")


if __name__ == "__main__":
    load_dotenv()

    example_request = {
        "event_type": "request",
        "payload": {
            "exhibition_id": 1,
            "request_value": 0,
            "time_at": datetime.now().isoformat()
        }
    }

    example_rating = {
        "event_type": "rating",
        "payload": {
            "exhibition_id": 1,
            "rating_value": 4,
            "time_at": datetime.now().isoformat()
        }
    }

    # load(example_request)
    # load(example_rating)
    # load(example_rating)
