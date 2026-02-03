from typing import List

from pydantic import BaseModel

from position.models import Position


class PortfolioResponse(BaseModel):
    unrealized_pnl: float
    realized_pnl: float
    positions: List[Position]
