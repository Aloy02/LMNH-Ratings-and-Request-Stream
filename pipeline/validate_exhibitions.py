import pandas as pd
from logger import setup_logger

EXPECTED_COLUMNS = {
    'EXHIBITION_NAME',
    'EXHIBITION_ID',
    'FLOOR',
    'DEPARTMENT',
    'START_DATE',
    'DESCRIPTION'
}


logger = setup_logger()


def validate_schema(df: pd.DataFrame) -> bool:
    """Validates that all required exhibition headers exist in the DataFrame."""
    df_cols = set(df.columns)
    missing_cols = EXPECTED_COLUMNS - df_cols
    extra_cols = df_cols - EXPECTED_COLUMNS

    if missing_cols:
        logger.error(
            f"validate_schema: Missing required columns: {sorted(list(missing_cols))}")
        return False

    if extra_cols:
        logger.warning(
            f"validate_schema: Found extra columns: {sorted(list(extra_cols))}")

    logger.info("validate_schema: Schema validation passed.")
    return True


def validate_exhibition_name(series: pd.Series) -> pd.Series:
    """Validates that EXHIBITION_NAME is a non-empty string."""
    invalid_mask = series.isna() | (series.astype(str).str.strip() == "")
    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        logger.warning(
            f"validate_exhibition_name: Found {invalid_count} row(s) with missing or empty names.")
    else:
        logger.info("validate_exhibition_name: All exhibition names are valid.")

    return invalid_mask


def validate_exhibition_id(series: pd.Series) -> pd.Series:
    """Validates that EXHIBITION_ID follows the 'EXH_XX' format (where XX is digits)."""
    id_pattern = r"^EXH_\d+$"
    invalid_mask = series.isna() | ~series.astype(str).str.match(id_pattern)
    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        logger.warning(
            f"validate_exhibition_id: Found {invalid_count} row(s) with invalid ID format (expected 'EXH_XX').")
    else:
        logger.info(
            "validate_exhibition_id: All exhibition IDs match the required format.")

    return invalid_mask


VALID_FLOORS = {'1', '2', '3', 'Vault'}


def validate_floor(series: pd.Series) -> pd.Series:
    """Validates that FLOOR is one of the valid floor values (e.g., '1', 'Vault')."""
    invalid_mask = ~series.astype(str).isin(VALID_FLOORS)
    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        logger.warning(
            f"validate_floor: Found {invalid_count} row(s) with invalid floor values.")
    else:
        logger.info("validate_floor: All floor entries are valid.")

    return invalid_mask


def validate_department(series: pd.Series) -> pd.Series:
    """Validates that DEPARTMENT is a non-empty string."""
    invalid_mask = series.isna() | (series.astype(str).str.strip() == "")
    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        logger.warning(
            f"validate_department: Found {invalid_count} row(s) with missing department values.")
    else:
        logger.info("validate_department: All department entries are valid.")

    return invalid_mask


def validate_start_date(series: pd.Series) -> pd.Series:
    """Validates that START_DATE can be parsed as a date (e.g., '01/07/19' or '23/08/21')."""
    parsed_dates = pd.to_datetime(series, errors='coerce', format='%d/%m/%y')
    invalid_mask = parsed_dates.isna()
    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        logger.warning(
            f"validate_start_date: Found {invalid_count} row(s) with invalid date formats.")
    else:
        logger.info("validate_start_date: All start dates are valid.")

    return invalid_mask


def validate_description(series: pd.Series) -> pd.Series:
    """Validates that DESCRIPTION is a non-empty string."""
    invalid_mask = series.isna() | (series.astype(str).str.strip() == "")
    invalid_count = invalid_mask.sum()

    if invalid_count > 0:
        logger.warning(
            f"validate_description: Found {invalid_count} row(s) with missing descriptions.")
    else:
        logger.info("validate_description: All description entries are valid.")

    return invalid_mask


def validate_exhibitions_csv(exhibitions_file_path: str) -> bool:
    """
    Runs schema and row-level checks on the exhibitions DataFrame.
    Returns a report DataFrame containing boolean error flags for each check.
    """

    df = pd.read_csv(exhibitions_file_path)

    logger.info(
        f"Starting validation on exhibitions dataset containing {len(df)} rows.")

    if not validate_schema(df):
        logger.error(
            "Cannot proceed with row validation due to missing required schema columns.")
        return False

    report = pd.DataFrame(index=df.index)

    report['invalid_name'] = validate_exhibition_name(df['EXHIBITION_NAME'])
    report['invalid_id'] = validate_exhibition_id(df['EXHIBITION_ID'])
    report['invalid_floor'] = validate_floor(df['FLOOR'])
    report['invalid_department'] = validate_department(df['DEPARTMENT'])
    report['invalid_start_date'] = validate_start_date(df['START_DATE'])
    report['invalid_description'] = validate_description(df['DESCRIPTION'])

    report['has_error'] = report.any(axis=1)

    total_errors = report['has_error'].sum()
    if total_errors > 0:
        logger.error(
            f"Validation finished: {total_errors} out of {len(df)} rows failed validation.")
    else:
        logger.info(
            "Validation finished: All rows passed validation successfully.")

    return total_errors == 0
