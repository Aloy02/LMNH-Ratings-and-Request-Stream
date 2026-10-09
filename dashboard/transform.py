"""Transform kiosk data to a standard format."""
import json


def transform(kiosk_data: dict) -> dict:
    """Uniform the kiosk data to a standard format."""
    time_at = kiosk_data["at"]

    # Adjusting for 1-based indexing in the RDS
    exhibition_id = int(kiosk_data["site"]) + 1

    rating_value = kiosk_data["val"]
    request_value = kiosk_data.get("type")

    if 0 <= rating_value <= 4:
        return {"event_type": "rating",
                "payload": {"time_at": time_at, "exhibition_id": exhibition_id, "rating_value": rating_value}}

    return {"event_type": "request",
            "payload": {"time_at": time_at, "exhibition_id": exhibition_id, "request_value": request_value}}


if __name__ == "__main__":
    with open("good_consumer_logs.txt", "r", encoding="utf-8") as f:
        for line in f:
            kiosk_data = json.loads(line.strip())
            transformed_data = transform(kiosk_data)
            print(transformed_data)
