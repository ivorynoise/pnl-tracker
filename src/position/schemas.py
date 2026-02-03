from typing import Dict

from pydantic import BaseModel


class PositionResponse(BaseModel):
    symbol: str
    quantity: float
    avg_price: float
    realized_pnl: float


class AllPositionsResponse(BaseModel):
    positions: Dict[str, PositionResponse]
