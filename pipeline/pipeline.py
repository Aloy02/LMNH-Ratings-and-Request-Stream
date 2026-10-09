from validate_requests import validate_requests_csv
from validate_exhibitions import validate_exhibitions_csv
from extract import extract_to
from logger import setup_logger
from transform import transform
from load import load

request_file_path = "./raw_data/requests_raw_data.csv"
exhibition_file_path = "./raw_data/exhibition_raw_data.csv"


def pipeline(request_file_path: str, exhibition_file_path: str):
    logger = setup_logger()

    # EXTRACT

    extract_to(request_file_path, exhibition_file_path)

    # VALIDATE

    if not validate_requests_csv(request_file_path):
        logger.error("Request CSV validation failed.")
        return
    if not validate_exhibitions_csv(exhibition_file_path):
        logger.error("Exhibition CSV validation failed.")
        return

    # TRANSFORM

    exhibitions_df, ratings_df, requests_df = transform(
        exhibition_file_path, request_file_path)

    # LOAD

    load("exhibitions", exhibitions_df)
    load("ratings", ratings_df)
    load("requests", requests_df)


if __name__ == "__main__":

    pipeline(request_file_path, exhibition_file_path)
