# Validation functions for the museum data pipeline
import pandas as pd
from logger import setup_logger

logger = setup_logger()


def validate_at(series: pd.Series) -> pd.Series:
    """Validates that values can be parsed into standard datetimes.

    Times that are before 8:45 AM and after 6:15 PM are to be removed as the
    exhibition manager has stated these happen by employees and therefore should be discounted.
    These should not fail the validation but be instead removed during transformation.

    """
    parsed_at = pd.to_datetime(series, errors='coerce')
    invalid_mask = parsed_at.isna()

    invalid_time_mask = (parsed_at.dt.time < pd.to_datetime("08:45:00").time()) | (
        parsed_at.dt.time > pd.to_datetime("18:15:00").time())

    invalid_time_count = invalid_time_mask.sum()

    if invalid_time_count > 0:
        logger.warning(
            f"validate_at: Found {invalid_time_count} row(s) with times outside the valid range.")
    else:
        logger.debug(
            "validate_at: All 'at' timestamps are within the valid time range.")

    invalid_count = invalid_mask.sum()
    if invalid_count > 0:
        logger.warning(
            f"validate_at: Found {invalid_count} row(s) with invalid datetimes.")
    else:
        logger.debug("validate_at: All 'at' timestamps are valid.")

    return invalid_mask


def validate_site(series: pd.Series) -> pd.Series:
    """Validates that site is an integer between 0 and 5 inclusive."""
    invalid_mask = ~series.isin(range(0, 6))

    invalid_count = invalid_mask.sum()
    if invalid_count > 0:
        logger.warning(
            f"validate_site: Found {invalid_count} row(s) with out-of-bounds site values.")
    else:
        logger.debug("validate_site: All 'site' IDs are valid.")

    return invalid_mask


def validate_val(series: pd.Series) -> pd.Series:
    """Validates that val is a number between -1 and 4 inclusive."""
    invalid_mask = ~series.between(-1, 4)

    invalid_count = invalid_mask.sum()
    if invalid_count > 0:
        logger.warning(
            f"validate_val: Found {invalid_count} row(s) with out-of-bounds val values.")
    else:
        logger.debug("validate_val: All 'val' numbers are valid.")

    return invalid_mask


def validate_type(type_series: pd.Series, val_series: pd.Series) -> pd.Series:
    """
    Validates conditional logic for type:
    - If val == -1, type must be 0 or 1.
    - If val != -1, type must be NaN/missing.
    """
    val_is_neg1 = val_series == -1

    valid_type_neg1 = val_is_neg1 & type_series.isin([0, 1])
    valid_type_other = (~val_is_neg1) & type_series.isna()

    invalid_mask = ~(valid_type_neg1 | valid_type_other)

    invalid_count = invalid_mask.sum()
    if invalid_count > 0:
        logger.warning(
            f"validate_type: Found {invalid_count} row(s) violating conditional type rules.")
    else:
        logger.debug(
            "validate_type: All 'type' values satisfy conditional logic rules.")

    return invalid_mask


def validate_requests_csv(file_path: str) -> bool:
    """Validates the requests CSV file and returns True if all rows pass validation, False otherwise."""
    df = pd.read_csv(file_path)

    logger.info(f"Starting validation on dataset containing {len(df)} rows.")

    if not validate_schema(df):
        logger.error("Request CSV schema validation failed.")
        return False

    report = pd.DataFrame(index=df.index)

    report['invalid_at'] = validate_at(df['at'])
    report['invalid_site'] = validate_site(df['site'])
    report['invalid_val'] = validate_val(df['val'])
    report['invalid_type'] = validate_type(df['type'], df['val'])

    report['has_error'] = report.any(axis=1)

    total_errors = report['has_error'].sum()
    if total_errors > 0:
        logger.warning(
            f"Validation finished: {total_errors} out of {len(df)} rows failed validation.")
    else:
        logger.info(
            "Validation finished: All rows passed validation successfully.")

    return total_errors == 0


def validate_schema(df: pd.DataFrame) -> bool:
    """
    Validates that all required headers/columns exist in the DataFrame.
    Logs missing or extra columns if found.
    """
    EXPECTED_COLUMNS = {'at', 'site', 'val', 'type'}
    df_cols = set(df.columns)

    missing_cols = EXPECTED_COLUMNS - df_cols
    extra_cols = df_cols - EXPECTED_COLUMNS

    if missing_cols:
        logger.error(
            f"validate_schema: Missing required columns: {list(missing_cols)}")
        return False

    if extra_cols:
        logger.warning(
            f"validate_schema: Found unexpected columns: {list(extra_cols)}")

    logger.info(
        "validate_schema: Schema validation passed. All required columns exist.")
    return True
