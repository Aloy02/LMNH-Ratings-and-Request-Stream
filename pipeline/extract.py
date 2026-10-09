""" Extracts historical satisfaction and exhibition data from an S3 bucket and saves them to local CSV files. """
from dotenv import dotenv_values
from boto3 import client, session
import re
import pandas as pd
import json

config = dotenv_values(".env")
BUCKET_NAME = 'sigma-resources-museum'


def get_museum_file_names(s3_client: session.Session.client, bucket_name: str):
    """ Retrieve the list of file names from the specified S3 bucket. """
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if "Contents" not in response:
        raise ValueError("No files found or bucket is empty.")

    return [file['Key'] for file in response["Contents"]]


def history_file_names(file_names: list[str]) -> list[str]:
    """ Returns a sorted list of history file names from the given list of file names. """
    history_file_names = []
    pattern = r"lmnh_hist_data_-?\d+.csv"

    for file_name in file_names:
        if re.match(pattern, file_name):
            history_file_names.append(file_name)

    history_file_names.sort(key=lambda filename: int(
        re.search(r"-?\d+", filename).group()))

    return history_file_names


def exhibition_file_names(file_names: list[str]) -> list[str]:
    """ Returns a list of exhibition file names from the given list of file names. """
    exhibition_file_names = []
    pattern = r"lmnh_exhibition_\w+.json"

    for file_name in file_names:
        if re.match(pattern, file_name):
            exhibition_file_names.append(file_name)

    return exhibition_file_names


def download_satisfaction_data(s3_client: session.Session.client, bucket_name: str, history_files: list[str]):
    """ Download historical data from S3 and combine them into a single dataset. """
    combined_data = []

    for file_name in history_files:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        df = pd.read_csv(response["Body"])
        combined_data.append(df)

    combined_data = pd.concat(combined_data, ignore_index=True)

    combined_data = combined_data.reset_index(drop=True)

    return combined_data


def download_exhibition_data(s3_client: session.Session.client, bucket_name: str, history_files: list[str]):
    """ Download exhibition data from S3 and combine them into a single dataset. """
    combined_data = []

    for file_name in history_files:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        data = json.loads(response["Body"].read().decode("utf-8"))

        df = pd.DataFrame([data])

        combined_data.append(df)

    return pd.concat(combined_data, ignore_index=True)


def get_historical_data(s3_client: session.Session.client, file_names: list[str]) -> pd.DataFrame:
    """ Retrieves and combines historical satisfaction data from S3. """
    history_files = history_file_names(file_names)
    combined_data = download_satisfaction_data(
        s3_client, BUCKET_NAME, history_files)

    combined_data['at'] = pd.to_datetime(combined_data['at'])

    return combined_data


def get_exhibition_data(s3_client: session.Session.client, file_names: list[str]) -> pd.DataFrame:
    """ Retrieves and combines exhibition data from S3. """

    exhibition_names = exhibition_file_names(file_names)

    exhibitions = download_exhibition_data(
        s3_client, BUCKET_NAME, exhibition_names)

    return exhibitions


def extract_to(request_file_path, exhibition_file_path):
    """ Extracts historical satisfaction and exhibition data from S3 and saves them to local CSV files. """
    s3_client = client('s3',
                       aws_access_key_id=config["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=config["AWS_SECRET_ACCESS_KEY"])

    file_names = get_museum_file_names(s3_client, BUCKET_NAME)
    requests_raw_data = get_historical_data(s3_client, file_names)
    exhibition_raw_data = get_exhibition_data(s3_client, file_names)

    requests_raw_data.to_csv(request_file_path, index=False)
    exhibition_raw_data.to_csv(exhibition_file_path, index=False)
    return requests_raw_data, exhibition_raw_data


if __name__ == "__main__":

    extract_to('./raw_data/requests_raw_data.csv',
               './raw_data/exhibition_raw_data.csv')
