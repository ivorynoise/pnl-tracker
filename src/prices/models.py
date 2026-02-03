from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class Price(BaseModel):
    symbol: str
    price: float
    timestamp: datetime


class PriceStore:
    # singleton store for prices
    # mimics Live Feed
    _instance: Optional["PriceStore"] = None
    prices: Dict[str, Price] = {}

    def __new__(cls) -> "PriceStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.prices = {}
        return cls._instance

    def update_price(self, symbol: str, price: float) -> Price:
        """Update or add a price for a symbol."""
        price_obj = Price(
            symbol=symbol,
            price=price,
            timestamp=datetime.now()
        )
        self.prices[symbol] = price_obj
        return price_obj

    def get_price(self, symbol: str) -> Optional[Price]:
        """Get the current price for a symbol."""
        return self.prices.get(symbol)

    def get_all_prices(self) -> Dict[str, Price]:
        """Get all current prices."""
        return self.prices


# Global singleton instance to mimic database or datastore 
price_store = PriceStore()
