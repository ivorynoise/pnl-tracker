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

    def add_long(self, trade: Trade):
        # adds to position store
        pass

    def add_short(self, trade: Trade):
        # adds to position store
        pass