from collections import defaultdict
from datetime import date
from src.file_watcher import HourlySalesCsvHandler
from statistics import mean, stdev

class SalesService:
    """Service layer for managing sales data and reporting."""

    def __init__(self, hourly_sales_csv_handler: HourlySalesCsvHandler):
        """Initializes the SalesService with a CSV handler.

        Args:
            hourly_sales_csv_handler (HourlySalesCsvHandler): Handler managing hourly sales data.
        """
        self.hourly_sales_csv_handler = hourly_sales_csv_handler

    def generate_report(self) -> dict:
        """Generates a complete report including totals, averages, trends, and outliers.

        Returns:
            dict: A dictionary containing:
                - "daily_totals": Total sales per day.
                - "avg_sales": Average sales per day.
                - "trends": Sales trends (sorted).
                - "outliers": Detected outlier sales per day.
        """
        return {
            "daily_totals": self.total_price_per_day(),
            "avg_sales": self.calculate_avg_sales(),
            "trends": self.sales_trend(),
            "outliers": self.detect_outliers()
        }

    def total_price_per_day(self) -> dict[date, float]:
        """Calculates total sales amount per day.

        Returns:
            dict[date, float]: Mapping of date to total sales amount.
        """
        result = {}
        data = self._get_sales_amount()
        for day, amount in data.items():
            result[day] = sum(amount)
        return result

    def calculate_avg_sales(self) -> dict[date, float]:
        """Calculates average sales amount per day.

        Returns:
            dict[date, float]: Mapping of date to average sales amount.
        """
        result = {}
        data = self._get_sales_amount()
        for day, amount in data.items():
            if amount:
                result[day] = self._avg(amount)
        return result

    def detect_outliers(self) -> dict[date, list[float]]:
        """Detects outlier sales values per day using standard deviation threshold.

        Returns:
            dict[date, list[float]]: Mapping of date to list of outlier sales values.
        """
        result: defaultdict[date, list[float]] = defaultdict(list)
        data = self._get_sales_amount()
        for day, amount in data.items():
            avg = self._avg(amount)
            outlier_threshold = avg + 1 * stdev(amount)
            for sale in amount:
                if sale > outlier_threshold:
                    result[day].append(sale)

        return dict(result)

    def sales_trend(self) -> list[tuple[date, float]]:
        """Returns sorted daily sales totals in descending order.

        Returns:
            list[tuple[date, float]]: List of (date, total sales) sorted by sales amount descending.
        """
        data = self.total_price_per_day()
        sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return sorted_data

    def _get_sales_amount(self) -> dict[date, list[float]]:
        """Retrieves all sales amounts grouped by day.

        Returns:
            dict[date, list[float]]: Mapping of date to list of sales amounts.
        """
        result = defaultdict(list)
        for day, sales_day in self.hourly_sales_csv_handler.store.items():
            for sales in sales_day.data.values():
                result[day].append(sales.sales_amount)

        return result

    def _avg(self, values: list[float]) -> float:
        """Calculates the average of a list of numbers.

        Args:
            values (list[float]): List of float values.

        Returns:
            float: Average value. Returns 0 if list is empty.
        """
        return sum(values) / len(values) if values else 0