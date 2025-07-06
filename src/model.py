from pydantic import BaseModel, Field
from datetime import date, time
from enum import StrEnum

class RegionDirection(StrEnum):
    """Enumeration for possible sales regions."""
    NORTH = "North"
    WEST = "West"
    EAST = "East"
    SOUTH = "South"

class HourlySales(BaseModel):
    """Model representing sales data for a specific hour.

    Attributes:
        sales_amount (float): The amount of sales. Must be greater than 0.
        product (str): Name of the product sold.
        region (RegionDirection): Directional region of the sale.
    """
    sales_amount: float = Field(..., gt=0)
    product: str = Field(...)
    region: RegionDirection

class SalesDay(BaseModel):
    """Model representing all sales within a single day, grouped by hour.

    Attributes:
        data (dict[time, HourlySales]): A mapping from time to HourlySales.
    """
    data: dict[time, HourlySales]

class SalesStore(BaseModel):
    """Model representing all recorded sales grouped by date.

    Attributes:
        days (dict[date, SalesDay]): A mapping from date to SalesDay.
    """
    days: dict[date, SalesDay]