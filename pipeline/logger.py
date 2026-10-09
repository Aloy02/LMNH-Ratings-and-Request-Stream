import argparse
import logging


def setup_logger() -> logging.Logger:
    """Configures logging level and format from command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Exhibitions CSV Data Validator")

    parser.add_argument(
        "-w", "--warning",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level (default: INFO)"
    )

    parser.add_argument(
        "-d", "--disable",
        action="store_true",
        help="Disable all log output."
    )

    args, _ = parser.parse_known_args()
    logger = logging.getLogger(__name__)

    if args.disable:
        logging.disable(logging.CRITICAL)
        return logger

    warning_val = args.warning or "INFO"
    log_level = getattr(logging, warning_val.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S"
    )

    return logger
