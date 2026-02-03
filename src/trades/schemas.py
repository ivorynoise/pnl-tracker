from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel

from trades.models import TradeSide


class TradeCreate(BaseModel):
    id: str
    symbol: str
    side: TradeSide
    price: Decimal
    quantity: Decimal
    timestamp: datetime


class TradeResponse(BaseModel):
    id: str
    symbol: str
    side: TradeSide
    price: Decimal
    quantity: Decimal
    timestamp: datetime


class TradeListResponse(BaseModel):
    trades: List[TradeResponse]
