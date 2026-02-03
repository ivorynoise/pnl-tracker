from datetime import datetime
from decimal import Decimal
from typing import Annotated, List

from pydantic import BaseModel, Field

from trades.models import TradeSide


# Annotated Decimal type with example for OpenAPI
DecimalField = Annotated[Decimal, Field(examples=["100.50"])]


class TradeCreate(BaseModel):
    id: str = Field(examples=["trade-001"])
    symbol: str = Field(examples=["BTCUSD"])
    side: TradeSide
    price: DecimalField
    quantity: DecimalField
    timestamp: datetime


class TradeResponse(BaseModel):
    id: str = Field(examples=["trade-001"])
    symbol: str = Field(examples=["BTCUSD"])
    side: TradeSide
    price: DecimalField
    quantity: DecimalField
    timestamp: datetime


class TradeListResponse(BaseModel):
    trades: List[TradeResponse]
