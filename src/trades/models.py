from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class TradeSide(str, Enum):
    BUY = "buy"
    SELL = "sell"


class Trade(BaseModel):
    id: str
    symbol: str
    side: TradeSide
    price: Decimal
    quantity: Decimal
    timestamp: datetime


class TradeStore:
    # singleton store for trades
    # mimics Database
    _instance: Optional["TradeStore"] = None

    def __new__(cls) -> "TradeStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.trades = []
        return cls._instance

    trades: List[Trade] = []

    def add_trade(self, trade: Trade) -> Trade:
        """Add a trade to the store."""
        self.trades.append(trade)
        return trade

    def get_all_trades(self) -> List[Trade]:
        """Get all trades."""
        return self.trades

    def get_trades_by_symbol(self, symbol: str) -> List[Trade]:
        """Get all trades for a specific symbol."""
        return [t for t in self.trades if t.symbol == symbol]


# Global singleton instance
trade_store = TradeStore()
