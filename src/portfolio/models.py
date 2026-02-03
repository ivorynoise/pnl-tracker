from decimal import Decimal
from typing import Optional


class PortfolioService:
    """Service to aggregate portfolio data from positions and prices."""

    _instance: Optional["PortfolioService"] = None

    def __new__(cls) -> "PortfolioService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_total_realized_pnl(self) -> Decimal:
        """Get total realized PnL across all positions."""
        from position.models import position_store

        total = Decimal("0")
        for position in position_store.get_all_positions().values():
            total += position.realized_pnl
        return total

    def get_total_unrealized_pnl(self) -> Decimal:
        """Get total unrealized PnL across all positions using current prices."""
        from position.models import position_store
        from prices.models import price_store

        total = Decimal("0")
        for symbol, position in position_store.get_all_positions().items():
            if position.quantity == 0:
                continue

            price = price_store.get_price(symbol)
            if price:
                unrealized = position_store.calculate_unrealized_pnl(
                    symbol, Decimal(str(price.price))
                )
                total += unrealized
        return total

    def get_position_unrealized_pnl(self, symbol: str) -> Decimal:
        """Get unrealized PnL for a specific position."""
        from position.models import position_store
        from prices.models import price_store

        position = position_store.get_position(symbol)
        if not position or position.quantity == 0:
            return Decimal("0")

        price = price_store.get_price(symbol)
        if not price:
            return Decimal("0")

        return position_store.calculate_unrealized_pnl(
            symbol, Decimal(str(price.price))
        )


# Global singleton instance to mimic database or datastore 
portfolio_service = PortfolioService()
