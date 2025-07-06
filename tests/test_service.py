from unittest.mock import MagicMock, patch
from src.service import SalesService

@patch("src.service.show_sales_store")
def test_sales_service_generate_report(mock_show_sales_store: MagicMock) -> None:
    mock_handler = MagicMock()
    service = SalesService(mock_handler)
    service.generate_report()
    mock_show_sales_store.assert_called_once()