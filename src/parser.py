from src.io.reader import CsvReader
from datetime import time, datetime
from typing import Type, Callable
from src.model import HourlySales
from pydantic import BaseModel
from pathlib import Path

class CsvModelParser[K, V: BaseModel]:
    """Generic CSV parser converting rows to Pydantic models.

    Args:
        model (Type[V]): Pydantic model class used to parse each row.
        key_func (Callable[[dict[str,str]], K]): Function to extract key from a CSV row.
        reader (CsvReader[K]): CSV reader instance.
        delimiter (str, optional): CSV delimiter. Defaults to ';'.
    """

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
        """Parses a CSV file into a dictionary of model instances.

        Args:
            path (Path): Path to the CSV file.

        Returns:
            dict[K, V]: Dictionary mapping keys to model instances.

        Raises:
            ValueError: If parsing a row fails.
        """
        raw_data = self.reader.read(path, self.key_func)
        result: dict[K, V] = {}

        for key, row in raw_data.items():
            try:
                result[key] = self.model(**row)
            except Exception as e:
                raise ValueError(f"Error parsing row {row} in file {path.name} {e}")

        return result

class HourlySalesCsvParser(CsvModelParser[time, HourlySales]):
    """Parser specialized for HourlySales CSV data."""

    def __init__(self, reader: CsvReader[time], key_name: str) -> None:
        """Initializes the parser with a key name for the time field.

        Args:
            reader (CsvReader[time]): CSV reader instance.
            key_name (str): The CSV column name used as key (parsed as time).
        """
        super().__init__(
            model=HourlySales,
            key_func=lambda row: datetime.strptime(row[key_name], "%H:%M").time(),
            reader=reader
        )