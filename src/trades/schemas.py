from datetime import datetime
from typing import List

from pydantic import BaseModel

from trades.models import TradeSide


class TradeCreate(BaseModel):
    id: str
    symbol: str
    side: TradeSide
    price: float
    quantity: float
    timestamp: datetime


class TradeResponse(BaseModel):
    id: str
    symbol: str
    side: TradeSide
    price: float
    quantity: float
    timestamp: datetime


class TradeListResponse(BaseModel):
    trades: List[TradeResponse]
