from src.io.reader import CsvReader
from datetime import time, datetime
from typing import Type, Callable
from src.model import HourlySales
from pydantic import BaseModel
from pathlib import Path

class CsvModelParser[K, V: BaseModel]:
    def __init__(self,
                 model: Type[V],
                 key_func: Callable[[dict[str,str]], K],
                 reader: CsvReader[K],
                 delimiter: str = ";") -> None:

        self.model = model
        self.key_func = key_func
        self.reader = reader
        self.delimiter = delimiter

    def parse(self, path: Path) -> dict[K, V]:
        raw_data = self.reader.read(path, self.key_func)
        result: dict[K, V] = {}

        for key, row in raw_data.items():
            try:
                result[key] = self.model(**row)
            except Exception as e:
                raise ValueError(f"Error parsing row {row} in file {path.name} {e}")

        return result

class HourlySalesCsvParser(CsvModelParser[time, HourlySales]):
    def __init__(self, reader: CsvReader[time], key_name: str) -> None:
        super().__init__(
            model=HourlySales,
            key_func=lambda row: datetime.strptime(row[key_name], "%H:%M").time(),
            reader=reader
        )