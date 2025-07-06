from src.utils import parse_date_from_filename, parse_time_from_row, show_sales_store
from src.model import SalesDay, RegionDirection, HourlySales
from _pytest.capture import CaptureFixture
from datetime import date, time

def test_parse_date_from_filename_valid() -> None:
    assert parse_date_from_filename("2025-07-05") == date(2025,7,5)

def test_parse_time_row_valid() -> None:
    row = {"hour": "15:05"}
    assert parse_time_from_row(row) == time(15, 5)

def test_show_sales_store_output(capsys: CaptureFixture[str]) -> None:
    sd = SalesDay(data={
        time(12,30): HourlySales(sales_amount=150, product="Widget A", region=RegionDirection.EAST)
    })

    store: dict[date, SalesDay] = {date(2025,7,5): sd}
    show_sales_store(store)

    out = capsys.readouterr().out

    assert "2025-07-05" in out
    assert "12:30" in out

