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

        total = Decimal("0")
        for symbol, position in position_store.get_all_positions().items():
            if position.quantity == 0:
                continue
            total += position_store.get_unrealized_pnl(symbol)
        return total


# Global singleton instance to mimic database or datastore
portfolio_service = PortfolioService()
