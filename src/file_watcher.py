from collections.abc import MutableMapping
from pathlib import Path
from typing import Callable
from pydantic import BaseModel
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from src.model import HourlySales, SalesDay, SalesStore
from src.parser import CsvModelParser
from datetime import datetime, date, time
import logging

logging.basicConfig(level=logging.INFO)


class CsvHandler[T: BaseModel, K, I, V: BaseModel](FileSystemEventHandler):
    def __init__(self,
                 store: MutableMapping[K, V],
                 parser: CsvModelParser[I, T],
                 key_func: Callable[[Path], K],
                 value_func: Callable[[dict[I, T]], V]
                 ) -> None:
        self.store = store
        self.parser = parser
        self.key_func = key_func
        self.value_func = value_func

    def on_created(self, event: FileSystemEvent):
        if self._should_ignore(event):
            return
        path = Path(str(event.src_path))
        key = self.key_func(path)
        if key in self.store:
            logging.info(f"Key {key} already exists skipping")
            return
        self._add_or_update(path, key, created=True)

    def on_deleted(self, event: FileSystemEvent):
        if self._should_ignore(event):
            return
        path = Path(str(event.src_path))
        key = self.key_func(path)
        if key in self.store:
            del self.store[key]
            logging.info(f"Key {key} deleted")
        else:
            logging.info(f"Key {key} does not exist")

    def on_modified(self, event: FileSystemEvent):
        if self._should_ignore(event):
            return
        path = Path(str(event.src_path))
        key = self.key_func(path)

        self._add_or_update(path, key, created=False)

    def _should_ignore(self, event: FileSystemEvent) -> bool:
        src_path = str(event.src_path)
        return event.is_directory or not src_path.endswith("csv")

    def _extract_key(self, path: Path) -> K:
        try:
            return self.key_func(path)
        except Exception as e:
            raise ValueError(f"Cannot extract key from path {e}")

    def _add_or_update(self, path: Path, key: K, *, created: bool) -> None:
        try:
            parser_data: dict[I, T] = self.parser.parse(path)
            value = self.value_func(parser_data)
            self.store[key] = value
            action = "created" if created else "updated"
            logging.info(f"{action} {key} with {len(parser_data)} entries")
        except Exception as e:
            logging.warning(f"Error while adding or updating {e}")


class HourlySalesCsvHandler(CsvHandler[HourlySales, date, time, SalesDay]):
    def __init__(self, store: SalesStore, parser: CsvModelParser[time, HourlySales]):

        def key_func(path: Path) -> date:
            return datetime.strptime(path.stem, "%Y-%m-%d").date()

        def value_func(data: dict[time, HourlySales]) -> SalesDay:
            return SalesDay(data=data)

        super().__init__(
            store = store.days,
            parser = parser,
            key_func= key_func,
            value_func = value_func
        )
