from src.file_watcher import HourlySalesCsvHandler
from src.utils import show_sales_store


class SalesService:
    def __init__(self, hourly_sales_csv_handler: HourlySalesCsvHandler):
        self.hourly_sales_csv_handler = hourly_sales_csv_handler

    def generate_report(self) -> None:
        show_sales_store(self.hourly_sales_csv_handler.store)


