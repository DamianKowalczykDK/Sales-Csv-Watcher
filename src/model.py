from enum import StrEnum
from datetime import date, time
from pydantic import BaseModel, Field

class RegionDirection(StrEnum):
    NORTH = 'North'
    WEST = 'West'
    EAST = 'East'
    SOUTH = 'South'

class HourlySales(BaseModel):
    sales_amount: float = Field(..., gt=0)
    product: str = Field(...)
    region: RegionDirection

class SalesDay(BaseModel):
    data: dict[time, HourlySales]

class SalesStore(BaseModel):
    days: dict[date, SalesDay]
