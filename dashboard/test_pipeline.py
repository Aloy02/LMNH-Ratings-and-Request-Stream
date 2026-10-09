"""Unit tests for the Kafka consumer module."""

from datetime import datetime
from pipeline import is_valid_message, decode_message


class SimpleMessage:
    """A simple message class to simulate Kafka Message behavior for testing."""

    def __init__(self, value=None, error=None):
        self._value = value
        self._error = error

    def value(self):
        """Return the message value."""
        return self._value

    def error(self):
        """Return the error, if any."""
        return self._error


class TestIsValidMessage():
    """Test cases for the is_valid_message function."""

    def test_is_valid_message_with_none(self):
        """Test that is_valid_message returns False when message is None."""
        result = is_valid_message(None)
        assert result == False

    def test_is_valid_message_with_valid_message(self):
        """Test that is_valid_message returns True for a message with no error."""
        msg = SimpleMessage(value=b'{"test": "data"}', error=None)
        result = is_valid_message(msg)
        assert result == True

    def test_is_valid_message_with_error(self):
        """Test that is_valid_message returns False when message has an error."""
        msg = SimpleMessage(value=None, error="Consumer error: timeout")
        result = is_valid_message(msg)
        assert result == False


class TestDecodeMessage():
    """Test cases for the decode_message function."""

    def test_decode_message_with_at_key(self):
        """Test decode_message when 'at' key is already present in JSON data."""
        json_data = b'{"at": "2024-01-01T10:00:00", "data": "test"}'
        msg = SimpleMessage(value=json_data, error=None)
        result = decode_message(msg)

        assert isinstance(result, dict)
        assert result["at"] == "2024-01-01T10:00:00"
        assert result["data"] == "test"

    def test_decode_message_without_at_key(self):
        """Test decode_message when 'at' key is missing from JSON data."""
        json_data = b'{"data": "test", "value": 123}'
        msg = SimpleMessage(value=json_data, error=None)
        result = decode_message(msg)

        assert isinstance(result, dict)
        assert "at" in result
        assert result["data"] == "test"
        assert result["value"] == 123
        # Verify 'at' is a valid ISO format datetime string
        datetime.fromisoformat(result["at"])
