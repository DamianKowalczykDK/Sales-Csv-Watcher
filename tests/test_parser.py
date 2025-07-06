from src.parser import CsvModelParser, HourlySalesCsvParser
from unittest.mock import MagicMock
from src.io.reader import CsvReader
from src.model import HourlySales
from pydantic import BaseModel
from datetime import time
from pathlib import Path
import pytest

class DummyParser(BaseModel):
    value: int

@pytest.fixture
def mock_parser_success() -> MagicMock:
    mock: MagicMock = MagicMock(spec=CsvReader[str])
    mock.read.return_value = {
        "row1": {"value": 100},
        "row2": {"value": 200}
    }
    return mock

@pytest.fixture
def mock_parser_fail() -> MagicMock:
    mock: MagicMock = MagicMock(spec=CsvReader[str])
    mock.read.return_value = {
        "badrow": "notanumber"
    }
    return mock

@pytest.fixture
def mock_hourly_sales_reader() -> MagicMock:
    mock: MagicMock = MagicMock(spec=CsvReader[time])
    mock.read.return_value = {
        time(10, 0): {
        "sales_amount": "100",
        "product": "Widget A",
        "region": "East"
    }
    }
    return mock

def test_csv_model_parser_success(mock_parser_success: CsvReader[str]) -> None:
    parser = CsvModelParser(
        model=DummyParser,
        key_func= lambda row: row["value"],
        reader=mock_parser_success
    )
    res = parser.parse(Path("dummy.csv"))

    assert res["row1"].value == 100
    assert res["row2"].value == 200

def test_csv_model_parser_fail(mock_parser_fail: CsvReader[str]) -> None:
    parser = CsvModelParser(
        model=DummyParser,
        key_func= lambda row: row["value"],
        reader=mock_parser_fail
    )

    with pytest.raises(ValueError) as e:
        parser.parse(Path("dummy.csv"))

    assert "notanumber" in str(e.value)

def test_hourly_sales_csv_parser_success(mock_hourly_sales_reader: CsvReader[time]) -> None:
    parser = HourlySalesCsvParser(reader=mock_hourly_sales_reader, key_name="hour")
    res = parser.parse(Path("dummy.csv"))

    sales = res[time(10, 0)]
    assert isinstance(sales, HourlySales)
    assert sales.sales_amount == 100
    assert sales.product == "Widget A"
    assert sales.region == "East"
