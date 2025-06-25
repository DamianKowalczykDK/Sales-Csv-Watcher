from pathlib import Path
from datetime import time, datetime
from pydantic import BaseModel
from typing import Type, Callable
from src.model import HourlySales
import csv


class CsvModelParser[K, V: BaseModel]:
    def __init__(self, model: Type[V], key_func: Callable[[dict[str,str]], K], delimiter: str = ";"):
        self.model = model
        self.key_func = key_func
        self.delimiter = delimiter

    def parse(self, path: Path) -> dict[K, V]:
        result: dict[K, V] = {}

        with path.open(newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            for row in reader:
                try:
                    key = self.key_func(row)
                    model_instance = self.model(**row)
                    result[key] = model_instance
                except Exception as e:
                    raise ValueError(f'Parse error: {e}')
        return result

class HourlySalesCsvParser(CsvModelParser[time, HourlySales]):
    def __init__(self):
        super().__init__(
            model=HourlySales,
            key_func=lambda row: datetime.strptime(row["hour"], "%H:%M").time()
        )