from typing import MutableMapping

from src.config import DATA_PATTERN, TIME_FORMAT, KEY_NAME
from datetime import time, date, datetime

from src.model import SalesStore, SalesDay


def parse_date_from_filename(filename: str) -> date:
    return datetime.strptime(filename, DATA_PATTERN).date()

def parse_time_from_row(row: dict[str, str]) -> time:
    return datetime.strptime(row[KEY_NAME], TIME_FORMAT).time()

def show_sales_store[K, V](sales_store: MutableMapping[K, V]) -> None:
    for key, value in sales_store.items():
        if isinstance(value, SalesDay):
            print(key)
            for hour, sales in value.data.items():
                print(hour)
                print(sales)