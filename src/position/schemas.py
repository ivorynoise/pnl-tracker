from decimal import Decimal
from typing import Dict

from pydantic import BaseModel


class PositionResponse(BaseModel):
    symbol: str
    quantity: Decimal
    avg_price: Decimal
    realized_pnl: Decimal


class AllPositionsResponse(BaseModel):
    positions: Dict[str, PositionResponse]
