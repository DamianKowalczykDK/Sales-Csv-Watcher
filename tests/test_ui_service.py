from unittest.mock import MagicMock, patch
from src.ui_service import UiService
from src.report_service import ReportService
import pytest

@pytest.fixture
def mock_service() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_report_service(mock_service: MagicMock) -> ReportService:
    return ReportService(service=mock_service)

@pytest.fixture
def mock_ui_service(mock_report_service: ReportService) -> UiService:
    return UiService(ui_service=mock_report_service)

@patch("src.ui_service.ReportService.report_total_price_per_day")
@patch("src.ui_service.st")
def test_show_ui_daily_total_sales(mock_st: MagicMock, mock_report: MagicMock,  mock_ui_service: UiService) -> None:
    mock_st.sidebar.radio.return_value = "Daily total sales"
    mock_st.sidebar.button.return_value = True
    mock_ui_service.show_ui()
    mock_report.assert_called_once()

@patch("src.ui_service.ReportService.report_calculate_avg_sales")
@patch("src.ui_service.st")
def test_show_ui_avg_sales(mock_st: MagicMock, mock_report: MagicMock, mock_ui_service: UiService) -> None:
    mock_st.sidebar.radio.return_value = "Avg sales"
    mock_st.sidebar.button.return_value = True
    mock_ui_service.show_ui()
    mock_report.assert_called_once()

@patch("src.ui_service.ReportService.report_sales_trend")
@patch("src.ui_service.st")
def test_show_ui_sales_trend(mock_st: MagicMock, mock_report: MagicMock, mock_ui_service: UiService) -> None:
    mock_st.sidebar.radio.return_value = "Trend sales"
    mock_st.sidebar.button.return_value = True
    mock_ui_service.show_ui()
    mock_report.assert_called_once()

@patch("src.ui_service.ReportService.report_detect_outliers")
@patch("src.ui_service.st")
def test_show_ui_outlier(mock_st: MagicMock, mock_report: MagicMock, mock_ui_service: UiService) -> None:
    mock_st.sidebar.radio.return_value = "Outlier"
    mock_st.sidebar.button.return_value = True
    mock_ui_service.show_ui()
    mock_report.assert_called_once()