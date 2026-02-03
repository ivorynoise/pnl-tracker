from datetime import datetime
from typing import Dict


class Price:
    symbol: str
    price: float
    timestamp: datetime


class PriceStore:
    # singleton store for prices
    # mimics Live Feed
    prices: Dict[str, Price] = {}
