"""Validation functions for kiosk data."""
from datetime import datetime, time
from logger import setup_logger
import json

logger = setup_logger()


def validate_kiosk_data(kiosk_data: dict) -> None:
    """Check if the kiosk data contains the required keys and valid datetime."""
    required_keys = ["site", "val"]

    for key in required_keys:
        if key not in kiosk_data:
            raise ValueError(f"Missing required key: {key}")
    try:
        datetime.fromisoformat(kiosk_data.get("at"))
    except ValueError:
        raise ValueError("Invalid datetime format for 'at' field.")

    if not isinstance(kiosk_data.get("val"), int):
        raise ValueError(f"Invalid value for 'val': {kiosk_data['val']}")

    try:
        site = int(kiosk_data.get("site"))
    except (TypeError, ValueError):
        raise ValueError(f"Invalid value for 'site': {kiosk_data['site']}")

    if not (0 <= site <= 5):
        raise ValueError(f"Invalid value for 'site': {site}")

    if kiosk_data["val"] == -1:
        if "type" not in kiosk_data:
            raise ValueError("Missing required key: type when val is -1")
        if not isinstance(kiosk_data["type"], int):
            raise ValueError(f"Invalid value for 'type': {kiosk_data['type']}")
        if kiosk_data["type"] not in [0, 1]:
            raise ValueError(f"Invalid value for 'type': {kiosk_data['type']}")

    if not (-1 <= kiosk_data["val"] <= 4):
        raise ValueError(f"Invalid value for 'val': {kiosk_data['val']}")

    start_time = time(8, 45)
    end_time = time(18, 15)

    at_time = datetime.fromisoformat(kiosk_data["at"]).time()
    if not (start_time <= at_time <= end_time):
        raise ValueError(f"Time out of range for 'at': {kiosk_data['at']}")


def is_valid(kiosk_data: dict) -> bool:
    try:
        validate_kiosk_data(kiosk_data)
    except Exception as e:
        logger.error(
            f"| {e} | {kiosk_data}")
        return False
    return True
