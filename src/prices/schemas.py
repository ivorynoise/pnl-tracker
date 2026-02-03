from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class PriceUpdate(BaseModel):
    price: float


class PriceResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime


class AllPricesResponse(BaseModel):
    prices: Dict[str, PriceResponse]
