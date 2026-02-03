from typing import List

from pydantic import BaseModel


class PositionSchema(BaseModel):
    symbol: str
    quantity: float
    avg_price: float
    realized_pnl: float

    class Config:
        from_attributes = True


class PortfolioResponse(BaseModel):
    unrealized_pnl: float
    realized_pnl: float
    positions: List[PositionSchema]
