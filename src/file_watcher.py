from watchdog.events import FileSystemEventHandler, FileSystemEvent
from src.model import HourlySales, SalesDay, SalesStore
from collections.abc import MutableMapping
from datetime import datetime, date, time
from src.utils import show_sales_store
from src.parser import CsvModelParser
from pydantic import BaseModel
from typing import Callable
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class CsvHandler[T: BaseModel, K, I, V: BaseModel](FileSystemEventHandler):
    def __init__(self,
                 store: MutableMapping[K, V],
                 parser: CsvModelParser[I, T],
                 key_func: Callable[[Path], K],
                 value_func: Callable[[dict[I, T]], V],
                 watch_path: Path,
                 ) -> None:
        self.store = store
        self.parser = parser
        self.key_func = key_func
        self.value_func = value_func
        self._initialize_from_directory(watch_path)

    def on_created(self, event: FileSystemEvent):
        if self._should_ignore(event):
            return
        path = Path(str(event.src_path))
        key = self.key_func(path)
        if key in self.store:
            logger.warning(f"Key {key} already exists skipping")
            return
        self._add_or_update(path, key, created=True)
        show_sales_store(self.store)

    def on_deleted(self, event: FileSystemEvent):
        if self._should_ignore(event):
            return
        path = Path(str(event.src_path))
        key = self.key_func(path)
        if key in self.store:
            del self.store[key]
            logger.info(f"Key {key} deleted")
        else:
            logger.warning(f"Key {key} does not exist")
        show_sales_store(self.store)

    def on_modified(self, event: FileSystemEvent):
        if event.is_directory:
            return

        path = Path(str(event.src_path))
        key = self.key_func(path)

        if not path.name.endswith("csv"):
            if key in self.store:
                del self.store[key]
                logging.info(f"Deleted {key} when file name does not end with .csv")
            show_sales_store(self.store)
            return

        self._add_or_update(path, key, created=False)
        show_sales_store(self.store)

    def _should_ignore(self, event: FileSystemEvent) -> bool:
        src_path = str(event.src_path)
        return event.is_directory or not src_path.endswith("csv")

    def _extract_key(self, path: Path) -> K:
        try:
            return self.key_func(path)
        except Exception as e:
            logger.error(f"Cannot extract key from path {e}")
            raise ValueError(f"Cannot extract key from path {e}")

    def _add_or_update(self, path: Path, key: K, *, created: bool) -> None:
        try:
            parser_data: dict[I, T] = self.parser.parse(path)
            value = self.value_func(parser_data)
            self.store[key] = value
            action = "created" if created else "updated"
            logging.info(f"{action} {key} with {len(parser_data)} entries")
        except Exception as e:
            logging.error(f"Error file in {path.name} while adding or updating {e}")


    def _initialize_from_directory(self, watch_path: Path) -> None:
        if not watch_path.exists() or not watch_path.is_dir():
            logger.error(f"Watch path {watch_path} does not exist")
            return

        for path in watch_path.iterdir():
            if not path.is_file() or path.suffix != ".csv":
                continue

            try:
                key = self._extract_key(path)
                self._add_or_update(path, key, created=True)
                logging.info(f"Initialized {key}")
            except Exception as e:
                logger.error(f"Error in file {path.name} while initializing {e}")

        logger.info(f"Initialized {len(self.store)} entries")
        show_sales_store(self.store)



class HourlySalesCsvHandler(CsvHandler[HourlySales, date, time, SalesDay]):
    def __init__(self, store: SalesStore, parser: CsvModelParser[time, HourlySales], watch_path: Path) -> None:

        def key_func(path: Path) -> date:
            return datetime.strptime(path.stem, "%Y-%m-%d").date()

        def value_func(data: dict[time, HourlySales]) -> SalesDay:
            return SalesDay(data=data)

        super().__init__(
            store = store.days,
            parser = parser,
            key_func= key_func,
            value_func = value_func,
            watch_path=watch_path
        )
