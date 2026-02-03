from decimal import Decimal
from typing import Dict, Optional

from trades.models import Trade


class Position:
    def __init__(self, symbol: str = ""):
        self.symbol = symbol
        self.quantity = Decimal("0")  # positive = long, negative = short
        self.avg_price = Decimal("0")
        self.realized_pnl = Decimal("0")


class PositionStore:
    # singleton store for positions
    # mimics Database
    _instance: Optional["PositionStore"] = None

    def __new__(cls) -> "PositionStore":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.positions = {}
        return cls._instance

    positions: Dict[str, Position] = {}

    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol."""
        return self.positions.get(symbol)

    def get_all_positions(self) -> Dict[str, Position]:
        """Get all positions."""
        return self.positions

    def update_position(self, trade: Trade) -> Position:
        """Update position based on a trade."""
        symbol = trade.symbol
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol)

        position = self.positions[symbol]

        if trade.side.lower() == "buy":
            self._add_long(position, trade)
        else:
            self._add_short(position, trade)

        return position

    def _add_long(self, position: Position, trade: Trade) -> None:
        """Process a buy trade."""
        if position.quantity >= 0:
            # Adding to long position - update avg price
            total_cost = (position.quantity * position.avg_price) + (
                trade.quantity * trade.price
            )
            position.quantity += trade.quantity
            position.avg_price = (
                total_cost / position.quantity
                if position.quantity != 0
                else Decimal("0")
            )
        else:
            # Closing short position
            close_qty = min(trade.quantity, abs(position.quantity))
            # Realized PnL: sold high (avg_price), bought back low (trade.price)
            position.realized_pnl += close_qty * (position.avg_price - trade.price)

            remaining_qty = trade.quantity - close_qty
            position.quantity += close_qty

            if remaining_qty > 0:
                # Opening new long position with remaining
                position.quantity = remaining_qty
                position.avg_price = trade.price

    def _add_short(self, position: Position, trade: Trade) -> None:
        """Process a sell trade."""
        if position.quantity <= 0:
            # Adding to short position - update avg price
            total_cost = (abs(position.quantity) * position.avg_price) + (
                trade.quantity * trade.price
            )
            position.quantity -= trade.quantity
            position.avg_price = (
                total_cost / abs(position.quantity)
                if position.quantity != 0
                else Decimal("0")
            )
        else:
            # Closing long position
            close_qty = min(trade.quantity, position.quantity)
            # Realized PnL: bought low (avg_price), sold high (trade.price)
            position.realized_pnl += close_qty * (trade.price - position.avg_price)

            remaining_qty = trade.quantity - close_qty
            position.quantity -= close_qty

            if remaining_qty > 0:
                # Opening new short position with remaining
                position.quantity = -remaining_qty
                position.avg_price = trade.price

    def get_unrealized_pnl(self, symbol: str) -> Decimal:
        """Get unrealized PnL for a specific position using current price."""
        from prices.models import price_store

        position = self.positions.get(symbol)
        if not position or position.quantity == 0:
            return Decimal("0")

        price = price_store.get_price(symbol)
        if not price:
            return Decimal("0")

        current_price = Decimal(str(price.price))
        if position.quantity > 0:
            # Long: profit if price went up
            return position.quantity * (current_price - position.avg_price)
        else:
            # Short: profit if price went down
            return abs(position.quantity) * (position.avg_price - current_price)

    def get_realized_pnl(self, symbol: str) -> Decimal:
        """Get realized PnL for a symbol."""
        position = self.positions.get(symbol)
        return position.realized_pnl if position else Decimal("0")


# Global singleton instance to mimic database or datastore
position_store = PositionStore()
