from itertools import product
from unittest.mock import MagicMock, patch

from _pytest import mark
from datetime import date, time, datetime
from src import service
from src.model import SalesDay, HourlySales, RegionDirection, SalesStore
from src.service import SalesService
import pytest

@pytest.fixture
def mock() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_handler(mock: MagicMock, dummy_store: dict[date, SalesDay]) -> MagicMock:
    mock.store = dummy_store
    return mock

@pytest.fixture
def mock_service(mock_handler: MagicMock) -> SalesService:
    return SalesService(hourly_sales_csv_handler=mock_handler)

@pytest.fixture
def dummy_store() -> dict[date, SalesDay]:
    return  {
        date(2025, 7, 5): SalesDay(data={
            time(9,0): HourlySales(sales_amount=150, product="Widget A", region=RegionDirection.EAST),
            time(10, 0): HourlySales(sales_amount=150, product="Widget B", region=RegionDirection.NORTH)
        })
    }


def test_generate_report(mock: MagicMock, mock_service: SalesService) -> None:
    result = mock_service.generate_report()
    assert isinstance(result, dict)
    assert "daily_totals" in result
    assert "avg_sales" in result





@pytest.mark.parametrize("values, expected" ,[
     ([10, 20, 30], 20),
     ([100, 100], 100)
])
def test_avg(values: list[float], expected: int) -> None:
    service = SalesService(MagicMock())
    result = service._avg(values)
    assert result == expected

def test_get_sales_amount(mock: MagicMock, mock_service: SalesService) -> None:
    result = mock_service._get_sales_amount()
    assert result == {date(2025, 7, 5): [150, 150]}

def test_total_price_per_day(mock: MagicMock, mock_service: SalesService) -> None:
    result = mock_service.total_price_per_day()
    assert result == {date(2025, 7, 5): 300}

def test_calculate_avg_sales(mock: MagicMock, dummy_store, mock_service: SalesService) -> None:
    result = mock_service.calculate_avg_sales()
    assert result == {date(2025, 7, 5): 150}

def test_sales_trend(mock:MagicMock, mock_service: SalesService) -> None:
    mock.handler.store = {
        date(2025, 7, 5): SalesDay(data={
            time(9, 0): HourlySales(sales_amount=150, product="Widget A", region=RegionDirection.EAST),
            time(10, 0): HourlySales(sales_amount=150, product="Widget B", region=RegionDirection.NORTH)
        }),
        date(2025, 5, 5): SalesDay(data={
            time(9, 0): HourlySales(sales_amount=150, product="Widget A", region=RegionDirection.EAST),
            time(10, 0): HourlySales(sales_amount=150, product="Widget B", region=RegionDirection.NORTH)
        }),
    }
    service = SalesService(hourly_sales_csv_handler=mock.handler)
    result = service.sales_trend()
    assert result == [(date(2025,7,5), 300), (date(2025, 5, 5), 300)]

def test_detect_outliers(mock: MagicMock) -> None:
    mock.handler.store = {
        date(2025, 7, 5): SalesDay(data={
            time(9,0): HourlySales(sales_amount=100, product="Widget A", region=RegionDirection.EAST),
            time(10,0): HourlySales(sales_amount=110, product="Widget A", region=RegionDirection.NORTH),
            time(11,0): HourlySales(sales_amount=95, product="Widget B", region=RegionDirection.WEST),
            time(12,0): HourlySales(sales_amount=105, product="Widget C", region=RegionDirection.EAST),
            time(13,0): HourlySales(sales_amount=500, product="Widget A", region=RegionDirection.WEST),
            time(14,0): HourlySales(sales_amount=90, product="Widget B", region=RegionDirection.NORTH),
            time(15,0): HourlySales(sales_amount=85, product="Widget C", region=RegionDirection.EAST),
        })
    }
    service = SalesService(hourly_sales_csv_handler=mock.handler)
    result = service.detect_outliers()
    assert result == {date(2025,7,5): [500]}
