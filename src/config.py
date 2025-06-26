import argparse
from pathlib import Path
import logging

WATCH_DIR = Path("data")
DEFAULT_LOG_FILE = "sales.log"
CSV_DELIMITER = ";"
DATA_PATTERN = "%Y-%M-%D"
TIME_FORMAT = "%H:%M"
KEY_NAME = "hour"

def parse_arguments() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description="Watch directory for Csv Sales files")
    arg_parser.add_argument(
        "--dir",
        type=Path,
        default=WATCH_DIR,
        help="Directory to watch for Csv files (default: ./data)"
    )
    arg_parser.add_argument(
        "--logfile",
        type=str,
        default=DEFAULT_LOG_FILE,
        help="Optional log filename (default: ./logs)"
    )
    arg_parser.add_argument(
        "--key-name",
        type=str,
        default=KEY_NAME,
        help="Key name used in row parsing (default: hour)"
    )

    return arg_parser.parse_args()

def setup_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
    ])