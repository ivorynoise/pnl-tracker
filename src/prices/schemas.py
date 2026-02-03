from datetime import datetime
from decimal import Decimal
from typing import Annotated, Dict

from pydantic import BaseModel, Field


# Annotated Decimal type with example for OpenAPI
DecimalField = Annotated[Decimal, Field(examples=["41000.50"])]


class PriceUpdate(BaseModel):
    price: DecimalField


class PriceResponse(BaseModel):
    symbol: str = Field(examples=["BTCUSD"])
    price: DecimalField
    timestamp: datetime


class AllPricesResponse(BaseModel):
    prices: Dict[str, PriceResponse]
