from abc import ABC, abstractmethod
from typing import Callable
from pathlib import Path
import csv

class Reader[K, V](ABC):
    """Abstract base class defining an interface for reading data from a file.

    Type Variables:
        K: The type of the key in the returned dictionary.
        V: The type of the value in the returned dictionary.
    """

    @abstractmethod
    def read(self, path: Path, key_func: Callable[[V], K]) -> dict[K, V]:
        """Reads data from the given path and returns it as a dictionary.

        Args:
            path (Path): Path to the input file.
            key_func (Callable[[V], K]): Function that generates a key from a single record.

        Returns:
            dict[K, V]: A dictionary mapping keys to data records.
        """
        pass #pragma: no cover

class CsvReader[K](Reader[K, dict[str, str]]):
    """Reader implementation for reading data from CSV files."""

    def __init__(self, delimiter: str = ";"):
        """Initializes the CsvReader with the specified delimiter.

        Args:
            delimiter (str, optional): Delimiter used in the CSV file. Defaults to ';'.
        """
        self.delimiter = delimiter

    def read(self, path: Path, key_func: Callable[[dict[str, str]], K]) -> dict[K, dict[str, str]]:
        """Reads data from a CSV file and returns it as a dictionary.

        Args:
            path (Path): Path to the CSV file.
            key_func (Callable[[dict[str, str]], K]): Function that generates a key from each row.

        Returns:
            dict[K, dict[str, str]]: A dictionary where the key is the result of key_func(row),
            and the value is the dictionary representing a CSV row.
        """
        result: dict[K, dict[str, str]] = {}

        with path.open(newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=self.delimiter)
            for row in reader:
                key = key_func(row)
                result[key] = row
        return result