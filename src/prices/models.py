class Price:
    symbol: str
    price: float
    timestamp: datetime

class PriceStore:
    # singleton store for prices
    # mimics Live Feed
    prices: dict[str, Price] = {}