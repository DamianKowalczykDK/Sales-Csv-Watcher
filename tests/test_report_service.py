from unittest.mock import MagicMock
from datetime import date
import pytest
from pandas import DataFrame
from src.report_service import ReportService


@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_report_service(mock_service) -> ReportService:
    return ReportService(service=mock_service)

def test_report_total_price_per_day(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.total_price_per_day.return_value = {
        date(2025,7,5): 1000
    }
    result = mock_report_service.report_total_price_per_day()
    assert isinstance(result, DataFrame)
    assert len(result) == 1

def test_report_calculate_avg_sales(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.calculate_avg_sales.return_value = {
        date(2025,7,5): 150
    }
    result = mock_report_service.report_calculate_avg_sales()
    assert isinstance(result, DataFrame)
    assert len(result) == 1

def test_report_sales_trend(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.sales_trend.return_value = [
        (date(2025,7,5), 150),
        (date(2025,7,7), 850),
    ]
    result = mock_report_service.report_sales_trend()
    assert isinstance(result, DataFrame)
    assert len(result) == 2

def test_report_detect_outliers(mock_service: MagicMock, mock_report_service: ReportService) -> None:
    mock_service.detect_outliers.return_value = {
        date(2025,7,5): "500"
    }

    result = mock_report_service.report_detect_outliers()
    assert isinstance(result, DataFrame)
    assert len(result) == 1

