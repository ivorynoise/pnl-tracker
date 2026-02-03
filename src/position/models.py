from typing import Dict

from trades.models import Trade


class Position:
    def __init__(self):
        self.quantity = 0.0
        self.avg_price = 0.0
        self.realized_pnl = 0.0


class PositionStore:
    # singleton store for positions
    # mimics Database

    positions: Dict[str, Position] = {}

    def __init__(self):
        pass

    def get_position(self, symbol: str) -> Position:
        pass

    def get_all_positions(self) -> Dict[str, Position]:
        pass

    def update_position(self, trade: Trade):
        pass

    def add_long(self, trade: Trade):
        pass

    def add_short(self, trade: Trade):
        pass

    def calculate_unrealized_pnl(self, symbol: str, current_price: float) -> float:
        pass

    def calculate_realized_pnl(self, symbol: str) -> float:
        pass
