from datetime import datetime
from typing import List

from pydantic import BaseModel


class Trade(BaseModel):
    id: str
    symbol: str
    side: str  # buy / sell
    price: float
    quantity: float
    timestamp: datetime


class TradeStore(BaseModel):
    # singleton store for trades
    # mimics Database
    trades: List[Trade] = []

    def add_trade(self, trade: Trade):
        pass
