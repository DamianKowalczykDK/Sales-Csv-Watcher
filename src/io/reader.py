import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, override


class Reader[T](ABC):
    @abstractmethod
    def read(self, path: Path, key_func: Callable[[dict[str, str]], T]) -> dict[T, dict[str, str]]:
        pass

class CsvReader[T](Reader):
    def __init__(self, delimiter: str = ";"):
        self.delimiter = delimiter

    def read(self, path: Path, key_func: Callable[[dict[str, str]], T]) -> dict[T, dict[str, str]]:
        result = {}

        with path.open(newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            for row in reader:
                key = key_func(row)
                result[key] = row
        return result