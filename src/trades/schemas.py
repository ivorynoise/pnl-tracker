from datetime import datetime
from typing import List

from pydantic import BaseModel


class TradeCreate(BaseModel):
    id: str
    symbol: str
    side: str  # buy / sell
    price: float
    quantity: float
    timestamp: datetime


class TradeResponse(BaseModel):
    id: str
    symbol: str
    side: str
    price: float
    quantity: float
    timestamp: datetime


class TradeListResponse(BaseModel):
    trades: List[TradeResponse]
