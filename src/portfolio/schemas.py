class PortfolioResponse(BaseModel):
    unrealized_pnl: float
    realized_pnl: float
    positions: list[Position]