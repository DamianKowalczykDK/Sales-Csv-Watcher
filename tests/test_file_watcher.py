from src.model import HourlySales, SalesStore, SalesDay, RegionDirection
from src.file_watcher import CsvHandler, HourlySalesCsvHandler
from watchdog.events import FileSystemEvent
from src.parser import CsvModelParser
from unittest.mock import MagicMock
from datetime import time, date
from pydantic import BaseModel
from typing import Callable
from pathlib import Path
import logging
import pytest

class DummyModel(BaseModel):
    value: int

@pytest.fixture
def dummy_parser() -> MagicMock:
    mock: MagicMock = MagicMock(spec=CsvModelParser[str, DummyModel])
    mock.parse.return_value = {
        "1": DummyModel(value=1),
    }
    return mock

@pytest.fixture
def dummy_store() -> dict[str, DummyModel]:
    return {}

@pytest.fixture
def key_func() -> Callable[[Path], str]:
    return lambda path: path.stem

@pytest.fixture
def value_func() -> Callable[[dict[str, DummyModel]], DummyModel]:
    return lambda parsed: DummyModel(value=len(parsed))

@pytest.fixture
def dummy_watch_path(tmp_path: Path) -> Path:
    (tmp_path / 'file1.csv').write_text("test", "utf-8")
    (tmp_path / 'ignore.txt').write_text("ignore", "utf-8")
    return tmp_path

@pytest.fixture
def mock_parser() -> MagicMock:
    mock: MagicMock = MagicMock(spec=HourlySalesCsvHandler)
    mock.return_value = {
        time(12, 0): HourlySales(sales_amount=150, product="test", region=RegionDirection.EAST)
    }
    return mock

@pytest.fixture
def dummy_sales_store() -> SalesStore:
    return SalesStore(days={})

def test_hourly_sales_csv_handler(
        tmp_path: Path,
        mock_parser: MagicMock,
        dummy_sales_store: SalesStore,
) -> None:
    file_path = tmp_path / "2025-07-05.csv"
    file_path.write_text("test", "utf-8")

    handler = HourlySalesCsvHandler(
        store=dummy_sales_store,
        parser=mock_parser,
        watch_path=file_path,
    )
    key = handler.key_func(file_path)
    data = mock_parser()
    value = handler.value_func(data)

    dummy_sales_store.days[key] = value
    assert key == date(2025, 7, 5)
    assert isinstance(value, SalesDay)


def test_initialize_from_directory(
        dummy_parser: MagicMock,
        dummy_store: dict[str, DummyModel],
        key_func: Callable[[Path], str],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        dummy_watch_path: Path,
) -> None:
    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        watch_path=dummy_watch_path,
        key_func=key_func,
        value_func=value_func,
    )

    assert "file1" in dummy_store
    assert isinstance(dummy_store["file1"], DummyModel)

def make_fs_event(path: Path, is_dir: bool = False) -> MagicMock:
    event: MagicMock = MagicMock(spec=FileSystemEvent)
    event.src_path = str(path)
    event.is_directory = is_dir
    return event

def test_on_created_add_to_store(
        dummy_parser: MagicMock,
        dummy_store: dict[str, DummyModel],
        key_func: Callable[[Path], str],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        tmp_path: Path,
) -> None:
    file_path = tmp_path / "new.csv"
    file_path.touch()

    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        watch_path=tmp_path,
        key_func=key_func,
        value_func=value_func,
    )

    event = make_fs_event(file_path)
    handler.on_created(event)

    assert "new" in dummy_store
    dummy_parser.parse.assert_called_once_with(file_path)

def test_on_created_add_to_store_when_should_ignore(
        dummy_parser: MagicMock,
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        key_func: Callable[[Path], str],
        tmp_path: Path,
) -> None:
    tmp_path = tmp_path / "file.csv"
    tmp_path.touch()

    dummy_store: dict[str, DummyModel] = {"file": DummyModel(value=999)}

    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        key_func=key_func,
        value_func=value_func,
        watch_path=tmp_path,
    )
    event = make_fs_event(tmp_path, is_dir=True)
    handler.on_created(event)

    assert "file" in dummy_store

def test_on_deleted_from_store(
        dummy_parser: MagicMock,
        key_func: Callable[[Path], str],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        tmp_path: Path,
) -> None:
    dummy_store: dict[str, DummyModel] = {"file": DummyModel(value=1)}
    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        watch_path=tmp_path,
        key_func=key_func,
        value_func=value_func,
    )
    file_path = tmp_path / "file.csv"
    event = make_fs_event(file_path)
    handler.on_deleted(event)
    assert "file" not in dummy_store

def test_on_deleted_from_store_when_should_ignore(
        dummy_parser: MagicMock,
        key_func: Callable[[Path], str],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        tmp_path: Path,
) -> None:
    dummy_store: dict[str, DummyModel] = {"file": DummyModel(value=1)}
    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        key_func=key_func,
        value_func=value_func,
        watch_path=tmp_path,
    )

    file_path = tmp_path / "file.csv"
    event = make_fs_event(file_path, is_dir=True)
    handler.on_deleted(event)

    assert dummy_store["file"] == DummyModel(value=1)

def test_on_modified_updates_existing_when_key_already_present(
        dummy_parser: MagicMock,
        key_func: Callable[[Path], str],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        tmp_path: Path,
) -> None:
    dummy_store: dict[str, DummyModel] = {"file": DummyModel(value=999)}

    dummy_parser.parse.return_value = {
        "x": DummyModel(value=123),
    }

    file_path = tmp_path / "file.csv"
    file_path.touch()
    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        watch_path=tmp_path,
        key_func=key_func,
        value_func=value_func,
    )

    dummy_parser.parse.reset_mock()

    event = make_fs_event(file_path)
    handler.on_modified(event)

    assert "file" in dummy_store
    assert dummy_store["file"].value == 1

def test_on_modified_when_event_is_true(
        dummy_parser: MagicMock,
        key_func: Callable[[Path], str],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        tmp_path: Path,
) -> None:
    dummy_store: dict[str, DummyModel] = {"file": DummyModel(value=9)}

    dummy_parser.parse.return_value = {
        "x": DummyModel(value=12),
    }

    file_path = tmp_path / "file.csv"
    file_path.touch()
    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        watch_path=tmp_path,
        key_func=key_func,
        value_func=value_func,
    )

    dummy_parser.parse.reset_mock()

    event = make_fs_event(file_path, is_dir=True)
    handler.on_modified(event)

    assert "file" in dummy_store
    assert dummy_store["file"].value == 1

def test_add_or_update_logs_error_on_parse_failure(
        dummy_parser: MagicMock,
        dummy_store: dict[str, DummyModel],
        key_func: Callable[[Path], str],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
) -> None:
    file_path = tmp_path / "bad.csv"
    file_path.touch()

    dummy_parser.parse.side_effect = Exception("parse failed")

    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        watch_path=tmp_path,
        key_func=key_func,
        value_func=value_func,
    )

    event = make_fs_event(file_path)
    handler.on_created(event)
    assert "parse failed" in caplog.text
    assert "bad" not in dummy_store

def test_extract_key_raises_value_error_and_logs(
        dummy_parser: MagicMock,
        dummy_store: dict[str, DummyModel],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
) -> None:
    file_path = tmp_path / "bad.csv"
    file_path.touch()

    def broken_key_func(_: Path) -> str:
        raise RuntimeError("broken key")


    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        key_func=broken_key_func,
        value_func=value_func,
        watch_path=tmp_path,
    )

    assert "broken key" in caplog.text

def test_on_modified_deleted_non_csv_when_key_not_exist(
        dummy_parser: MagicMock,
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        key_func: Callable[[Path], str],
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
) -> None:
    file_path = tmp_path / "file.txt"
    file_path.touch()
    caplog.set_level(logging.INFO)

    dummy_store: dict[str, DummyModel] = {"file": DummyModel(value=123)}

    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        watch_path=tmp_path,
        key_func=key_func,
        value_func=value_func,
    )

    event = make_fs_event(file_path)
    handler.on_modified(event)

    assert "file" not in dummy_store
    assert "Deleted file when file name does not end with .csv" in caplog.text

def test_on_deleted_when_key_not_exist(
        dummy_parser: MagicMock,
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        key_func: Callable[[Path], str],
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
) -> None:

    file_path = tmp_path / "bad.csv"
    dummy_store: dict[str, DummyModel] = {}
    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        key_func=key_func,
        value_func=value_func,
        watch_path=tmp_path,
    )

    event = make_fs_event(file_path)
    handler.on_deleted(event)
    assert "Key bad does not exist" in caplog.text

def test_initialize_from_directory_logs_error_when_path_missing(
        dummy_parser: MagicMock,
        dummy_store: dict[str, DummyModel],
        value_func: Callable[[dict[str, DummyModel]], DummyModel],
        key_func: Callable[[Path], str],
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
) -> None:
    watch_path = tmp_path / "nonexistent"

    handler = CsvHandler[DummyModel, str, str, DummyModel](
        store=dummy_store,
        parser=dummy_parser,
        key_func=key_func,
        value_func=value_func,
        watch_path=watch_path,
    )

    assert "Watch path nonexistent does not exist"
