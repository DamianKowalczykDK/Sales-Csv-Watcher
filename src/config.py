from dotenv import load_dotenv
from pathlib import Path
import argparse
import logging
import os

load_dotenv()

WATCH_DIR = Path(os.getenv("WATCH_DIR", "./data"))
DEFAULT_LOG_FILE = os.getenv("DEFAULT_LOG_FILE", "sales.log")
CSV_DELIMITER = os.getenv("CSV_DELIMITER", ";")
DATA_PATTERN = os.getenv("DATA_PATTERN", "%Y-%m-%d")
TIME_FORMAT = os.getenv("TIME_FORMAT", "%H:%M")
KEY_NAME = os.getenv("KEY_NAME", "hour")

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
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            # logging.StreamHandler()
    ])