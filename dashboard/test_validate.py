"""Tests for validation functions in validate.py."""
import pytest
from validate import validate_kiosk_data, is_valid


class TestValidateKioskData:
    """Test cases for validate_kiosk_data function."""

    def test_valid_data_with_all_fields(self):
        """Test validation passes with all required fields and valid values."""
        valid_data = {
            "site": 2,
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        # Should not raise any exception
        validate_kiosk_data(valid_data)

    def test_valid_data_with_type_field(self):
        """Test validation passes when val is -1 and type is provided."""
        valid_data = {
            "site": 1,
            "val": -1,
            "at": "2024-01-15T10:30:00",
            "type": 0
        }
        validate_kiosk_data(valid_data)

    def test_valid_site_boundaries(self):
        """Test validation passes for all valid site values (0-5)."""
        for site in range(6):
            data = {
                "site": site,
                "val": 2,
                "at": "2024-01-15T10:30:00"
            }
            validate_kiosk_data(data)

    def test_valid_val_range(self):
        """Test validation passes for all valid val values (-1 to 4)."""
        for val in range(-1, 5):
            data = {
                "site": 2,
                "val": val,
                "at": "2024-01-15T10:30:00"
            }
            if val == -1:
                data["type"] = 0
            validate_kiosk_data(data)

    def test_valid_type_values(self):
        """Test validation passes for valid type values (0 and 1)."""
        for type_val in [0, 1]:
            data = {
                "site": 2,
                "val": -1,
                "at": "2024-01-15T10:30:00",
                "type": type_val
            }
            validate_kiosk_data(data)

    def test_missing_site_key(self):
        """Test validation fails when 'site' key is missing."""
        data = {
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Missing required key: site"):
            validate_kiosk_data(data)

    def test_missing_val_key(self):
        """Test validation fails when 'val' key is missing."""
        data = {
            "site": 2,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Missing required key: val"):
            validate_kiosk_data(data)

    def test_invalid_datetime_format(self):
        """Test validation fails with invalid datetime format."""
        data = {
            "site": 2,
            "val": 3,
            "at": "not-a-datetime"
        }
        with pytest.raises(ValueError, match="Invalid datetime format for 'at' field"):
            validate_kiosk_data(data)

    def test_invalid_val_not_integer(self):
        """Test validation fails when val is not an integer."""
        data = {
            "site": 2,
            "val": "three",
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Invalid value for 'val'"):
            validate_kiosk_data(data)

    def test_invalid_val_float(self):
        """Test validation fails when val is a float."""
        data = {
            "site": 2,
            "val": 3.5,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Invalid value for 'val'"):
            validate_kiosk_data(data)

    def test_invalid_site_not_integer(self):
        """Test validation fails when site cannot be converted to integer."""
        data = {
            "site": "two",
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Invalid value for 'site'"):
            validate_kiosk_data(data)

    def test_invalid_site_negative(self):
        """Test validation fails when site is negative."""
        data = {
            "site": -1,
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Invalid value for 'site': -1"):
            validate_kiosk_data(data)

    def test_invalid_site_too_large(self):
        """Test validation fails when site exceeds maximum (5)."""
        data = {
            "site": 6,
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Invalid value for 'site': 6"):
            validate_kiosk_data(data)

    def test_val_out_of_range_too_small(self):
        """Test validation fails when val is less than -1."""
        data = {
            "site": 2,
            "val": -2,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Invalid value for 'val': -2"):
            validate_kiosk_data(data)

    def test_val_out_of_range_too_large(self):
        """Test validation fails when val exceeds maximum (4)."""
        data = {
            "site": 2,
            "val": 5,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Invalid value for 'val': 5"):
            validate_kiosk_data(data)

    def test_missing_type_when_val_is_minus_one(self):
        """Test validation fails when val is -1 but type is missing."""
        data = {
            "site": 2,
            "val": -1,
            "at": "2024-01-15T10:30:00"
        }
        with pytest.raises(ValueError, match="Missing required key: type when val is -1"):
            validate_kiosk_data(data)

    def test_invalid_type_not_integer(self):
        """Test validation fails when type is not an integer."""
        data = {
            "site": 2,
            "val": -1,
            "at": "2024-01-15T10:30:00",
            "type": "zero"
        }
        with pytest.raises(ValueError, match="Invalid value for 'type'"):
            validate_kiosk_data(data)

    def test_invalid_type_out_of_range(self):
        """Test validation fails when type is not 0 or 1."""
        data = {
            "site": 2,
            "val": -1,
            "at": "2024-01-15T10:30:00",
            "type": 2
        }
        with pytest.raises(ValueError, match="Invalid value for 'type': 2"):
            validate_kiosk_data(data)

    def test_valid_iso_datetime_variants(self):
        """Test validation passes with various valid ISO datetime formats."""
        valid_datetimes = [
            "2024-01-15T10:30:00",
            "2024-12-31T23:59:59",
            "2000-01-01T00:00:00",
        ]
        for dt in valid_datetimes:
            data = {
                "site": 2,
                "val": 3,
                "at": dt
            }
            validate_kiosk_data(data)


class TestIsValid:
    """Test cases for is_valid function."""

    def test_returns_true_for_valid_data(self):
        """Test is_valid returns True for valid kiosk data."""
        valid_data = {
            "site": 2,
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        assert is_valid(valid_data) == True

    def test_returns_true_for_valid_data_with_type(self):
        """Test is_valid returns True when val is -1 and type is valid."""
        valid_data = {
            "site": 1,
            "val": -1,
            "at": "2024-01-15T10:30:00",
            "type": 0
        }
        assert is_valid(valid_data) == True

    def test_returns_false_for_missing_site(self):
        """Test is_valid returns False when site is missing."""
        data = {
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        assert is_valid(data) == False

    def test_returns_false_for_missing_val(self):
        """Test is_valid returns False when val is missing."""
        data = {
            "site": 2,
            "at": "2024-01-15T10:30:00"
        }
        assert is_valid(data) == False

    def test_returns_false_for_invalid_datetime(self):
        """Test is_valid returns False for invalid datetime."""
        data = {
            "site": 2,
            "val": 3,
            "at": "not-a-date"
        }
        assert is_valid(data) == False

    def test_returns_false_for_invalid_val_type(self):
        """Test is_valid returns False when val is not an integer."""
        data = {
            "site": 2,
            "val": "invalid",
            "at": "2024-01-15T10:30:00"
        }
        assert is_valid(data) == False

    def test_returns_false_for_invalid_site_range(self):
        """Test is_valid returns False when site is out of range."""
        data = {
            "site": 10,
            "val": 3,
            "at": "2024-01-15T10:30:00"
        }
        assert is_valid(data) == False

    def test_returns_false_for_invalid_val_range(self):
        """Test is_valid returns False when val is out of range."""
        data = {
            "site": 2,
            "val": 10,
            "at": "2024-01-15T10:30:00"
        }
        assert is_valid(data) == False

    def test_returns_false_for_missing_type_when_val_minus_one(self):
        """Test is_valid returns False when val is -1 but type is missing."""
        data = {
            "site": 2,
            "val": -1,
            "at": "2024-01-15T10:30:00"
        }
        assert is_valid(data) == False

    def test_returns_false_for_invalid_type_value(self):
        """Test is_valid returns False when type is invalid."""
        data = {
            "site": 2,
            "val": -1,
            "at": "2024-01-15T10:30:00",
            "type": 5
        }
        assert is_valid(data) == False

    def test_does_not_raise_exception(self):
        """Test is_valid never raises an exception (catches all errors)."""
        invalid_data = {
            "site": "invalid",
            "val": "invalid",
            "at": "invalid"
        }
        # Should return False without raising exception
        result = is_valid(invalid_data)
        assert result == False
