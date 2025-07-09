from src.service import SalesService
from pandas import DataFrame

class ReportService:
    """Service responsible for converting raw sales data into structured reports."""

    def __init__(self, service: SalesService):
        """Initializes the ReportService with a SalesService instance.

        Args:
            service (SalesService): The sales service providing raw sales data.
        """
        self.service = service

    def report_total_price_per_day(self) -> DataFrame:
        """Generates a report of total sales per day.

        Returns:
            DataFrame: A DataFrame with columns ["Day", "Total sales"].
        """
        data = self.service.total_price_per_day()
        df = DataFrame([
            {"Day": day, "Total sales": total} for day, total in data.items()
        ])
        return df

    def report_calculate_avg_sales(self) -> DataFrame:
        """Generates a report of average sales per day.

        Returns:
            DataFrame: A DataFrame with columns ["Day", "Avg sales"].
        """
        data = self.service.calculate_avg_sales()
        df = DataFrame([
            {"Day": day, "Avg sales": avg} for day, avg in data.items()
        ])
        return df

    def report_sales_trend(self) -> DataFrame:
        """Generates a report showing sales trends (sorted by sales value descending).

        Returns:
            DataFrame: A DataFrame with columns ["Day", "Sales"], sorted by sales.
        """
        data = self.service.sales_trend()
        df = DataFrame([
            {"Day": day, "Sales": sales} for day, sales in data
        ])
        return df

    def report_detect_outliers(self) -> DataFrame:
        """Generates a report listing outlier sales per day.

        Returns:
            DataFrame: A DataFrame with columns ["Day", "Outlier"], where outliers are joined as a string.
        """
        data = self.service.detect_outliers()
        df = DataFrame([
            {"Day": day, "Outlier": ", ".join(map(str, outlier))} for day, outlier in data.items()
        ])
        return df