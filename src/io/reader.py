from abc import ABC, abstractmethod
from typing import Callable
from pathlib import Path
import csv

class Reader[K, V](ABC):
    @abstractmethod
    def read(self, path: Path, key_func: Callable[[V], K]) -> dict[K, V]:
        pass #pragma: no cover

class CsvReader[K](Reader[K, dict[str, str]]):
    def __init__(self, delimiter: str = ";"):
        self.delimiter = delimiter

    def read(self, path: Path, key_func: Callable[[dict[str, str]], K]) -> dict[K, dict[str, str]]:
        result: dict[K, dict[str, str]] = {}

        with path.open(newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            for row in reader:
                key = key_func(row)
                result[key] = row
        return result