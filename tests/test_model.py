from src.model import HourlySales, RegionDirection
from pydantic import ValidationError
import pytest

def test_hourly_sales_valid() -> None:
    sales = HourlySales(
        sales_amount=100,
        product="Widget A",
        region=RegionDirection.EAST
    )

    assert sales.sales_amount == 100
    assert sales.product == "Widget A"
    assert sales.region == RegionDirection.EAST

@pytest.mark.parametrize("sales_amount", [0, ...])
def test_hourly_sales_invalid_sales_amount(sales_amount: float) -> None:
    with pytest.raises(ValidationError):
        HourlySales(
            sales_amount=sales_amount,
            product="Widget A",
            region=RegionDirection.EAST
        )

