from src.config import DATA_PATTERN, TIME_FORMAT, KEY_NAME
from datetime import time, date, datetime
from typing import MutableMapping
from src.model import SalesDay

def parse_date_from_filename(filename: str) -> date:
    """Parses a date object from a filename string using the configured pattern.

    Args:
        filename (str): The filename string to parse.

    Returns:
        date: Parsed date object.
    """
    return datetime.strptime(filename, DATA_PATTERN).date()

def parse_time_from_row(row: dict[str, str]) -> time:
    """Parses a time object from a CSV row dictionary using the configured key and format.

    Args:
        row (dict[str, str]): The CSV row dictionary.

    Returns:
        time: Parsed time object.
    """
    return datetime.strptime(row[KEY_NAME], TIME_FORMAT).time()

def show_sales_store[K, V](sales_store: MutableMapping[K, V]) -> None:
    """Prints the contents of the sales store to the console.

    If the value is a SalesDay, prints the date and then each hour and associated sales.

    Args:
        sales_store (MutableMapping[K, V]): The sales store mapping keys to values.
    """
    for key, value in sales_store.items():
        if isinstance(value, SalesDay):
            print(key)
            for hour, sales in value.data.items():
                print(hour)
                print(sales)