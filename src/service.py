from src.file_watcher import HourlySalesCsvHandler
from src.utils import show_sales_store

class SalesService:
    """Service layer for managing sales data and reporting."""

    def __init__(self, hourly_sales_csv_handler: HourlySalesCsvHandler):
        """Initializes the SalesService with a CSV handler.

        Args:
            hourly_sales_csv_handler (HourlySalesCsvHandler): Handler managing hourly sales data.
        """
        self.hourly_sales_csv_handler = hourly_sales_csv_handler

    def generate_report(self) -> None:
        """Generates and displays a report of the current sales store."""
        show_sales_store(self.hourly_sales_csv_handler.store)