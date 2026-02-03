from decimal import Decimal
from typing import Annotated, List

from pydantic import BaseModel, Field


# Annotated Decimal type with example for OpenAPI
DecimalField = Annotated[Decimal, Field(examples=["100.50"])]


class PositionSchema(BaseModel):
    symbol: str = Field(examples=["BTCUSD"])
    quantity: DecimalField
    avg_price: DecimalField
    realized_pnl: DecimalField
    unrealized_pnl: DecimalField


class PortfolioResponse(BaseModel):
    total_unrealized_pnl: DecimalField
    total_realized_pnl: DecimalField
    positions: List[PositionSchema]


class PnLResponse(BaseModel):
    total_unrealized_pnl: DecimalField
    total_realized_pnl: DecimalField
    total_pnl: DecimalField
