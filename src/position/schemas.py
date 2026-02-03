from decimal import Decimal
from typing import Annotated, Dict

from pydantic import BaseModel, Field


# Annotated Decimal type with example for OpenAPI
DecimalField = Annotated[Decimal, Field(examples=["100.50"])]


class PositionResponse(BaseModel):
    symbol: str = Field(examples=["BTCUSD"])
    quantity: DecimalField
    avg_price: DecimalField
    realized_pnl: DecimalField


class AllPositionsResponse(BaseModel):
    positions: Dict[str, PositionResponse]
