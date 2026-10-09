""" Module for loading data into a PostgreSQL database using psycopg2. """
from psycopg2 import connect
from dotenv import dotenv_values
from psycopg2.extras import execute_values
import pandas as pd
from logger import setup_logger

config = dotenv_values(".env")

logger = setup_logger()

conn = connect(
    host=config["DB_HOST"],
    port=config["DB_PORT"],
    dbname=config["DB_NAME"],
    user=config["DB_USER"],
    password=config["DB_PASSWORD"]
)


def execute_dataframe(cursor, table_name, df, page_size=10000):
    """ Executes an insert operation for a given DataFrame into the specified table. """
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join([f'"{c}"' for c in df.columns])
    query = f"INSERT INTO {table_name} ({cols}) VALUES %s"
    try:
        logger.info(
            f"Executing insert for table {table_name} with {len(tuples)} rows.")
        execute_values(cursor, query, tuples, page_size=page_size)

        logger.info(f"Loaded data into table {table_name}")
        conn.commit()
    except Exception as e:
        logger.error(
            f"Exception occurred while inserting data into table {table_name}: {e}")
        conn.rollback()


def load(table_name: str, df: pd.DataFrame) -> None:
    with conn.cursor() as cursor:
        execute_dataframe(cursor, table_name, df)
