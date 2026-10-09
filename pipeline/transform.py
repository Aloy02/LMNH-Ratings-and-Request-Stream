# Transforms raw data into a cleaned format suitable to be loaded into the database
from dotenv import dotenv_values
import pandas as pd
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from logger import setup_logger
logger = setup_logger()


config = dotenv_values(".env")

conn = connect(
    host=config["DB_HOST"],
    port=config["DB_PORT"],
    dbname=config["DB_NAME"],
    user=config["DB_USER"],
    password=config["DB_PASSWORD"],
)


def get_floor_map() -> dict:
    """ Retrieves a mapping of floor names to their corresponding floor IDs from the database. """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM floors")
        floor_data = cursor.fetchall()
    floor_map = {row['floor_name']: row['floor_id'] for row in floor_data}
    return floor_map


def get_department_map() -> dict:
    """ Retrieves a mapping of department names to their corresponding department IDs from the database. """
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM departments")
        departments_data = cursor.fetchall()
    department_map = {row['department_name']: row['department_id']
                      for row in departments_data}
    return department_map


def format_exhibition_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ Formats the exhibition columns to match the database schema. """
    df = df.rename(
        columns={
            "DEPARTMENT": "department_name",
            "FLOOR": "floor_name",
            "EXHIBITION_NAME": "exhibition_name",
            "START_DATE": "start_date"
        }
    )
    df['start_date'] = pd.to_datetime(df['start_date'], format='%d/%m/%y')
    return df


def format_request_columns(df: pd.DataFrame) -> pd.DataFrame:
    """ Formats the request columns to match the database schema.
        Times before 8:45 AM and after 6:15 PM are considered invalid and should be removed.
    """
    requests_raw_df = df.copy()
    df = df.rename(
        columns={
            "site": "exhibition_id",
            "val": "rating_value",
            "at": "time_at",
            "type": "request_value"
        }
    )
    df['rating_value'] = df['rating_value'].astype(int)

    df['time_at'] = pd.to_datetime(
        df['time_at'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df = df.set_index('time_at')
    df = df.between_time("08:45:00", "18:15:00")
    df = df.reset_index()
    logger.info(
        f"Removed {len(requests_raw_df) - len(df)} rows outside the valid time range.")
    return df


def create_exhibitions(df: pd.DataFrame, floor_map: dict, department_map: dict) -> pd.DataFrame:
    """ Creates a DataFrame of exhibitions with their corresponding floor and department IDs. """
    df = df.copy()
    df['floor_id'] = df['floor_name'].map(floor_map)
    df['department_id'] = df['department_name'].map(department_map)
    return df[['department_id', 'floor_id', 'exhibition_name', 'start_date']].drop_duplicates().reset_index(drop=True)


def create_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """ Creates a DataFrame of ratings with valid rating values. """
    df = df.copy()
    df = df[df['rating_value'] >= 0]
    df = df[['exhibition_id', 'rating_value', 'time_at']]
    return df


def create_requests(df: pd.DataFrame) -> pd.DataFrame:
    """ Creates a DataFrame of requests with valid request values. """
    df = df.copy()
    df = df[df['request_value'] >= 0]
    df = df[['exhibition_id', 'request_value', 'time_at']]
    return df


def transform(exhibition_raw_data: str, requests_raw_data: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """ Transforms raw exhibition and request data into formatted DataFrames for exhibitions, ratings, and requests. """
    exhibition_raw_df = pd.read_csv(exhibition_raw_data)
    requests_raw_df = pd.read_csv(requests_raw_data)

    exhibition_formatted_data = format_exhibition_columns(exhibition_raw_df)
    requests_formatted_data = format_request_columns(requests_raw_df)

    floor_map = get_floor_map()
    department_map = get_department_map()

    exhibitions_df = create_exhibitions(
        exhibition_formatted_data, floor_map, department_map)

    ratings_df = create_ratings(requests_formatted_data)
    ratings_df['exhibition_id'] = ratings_df['exhibition_id'] + 1

    requests_df = create_requests(requests_formatted_data)
    requests_df['request_value'] = requests_df['request_value'].astype(int)
    requests_df['exhibition_id'] = requests_df['exhibition_id'] + 1

    return exhibitions_df, ratings_df, requests_df
