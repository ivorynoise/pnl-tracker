class Portfolio(BaseModel):
    # DB table for portfolio
    # mimics Database

    # Skipping user id for now as we are designing for single user
    # user_id: str 
    unrealized_pnl: float = 0.0
    realized_pnl: float = 0.0


    def update_unrealized_pnl(self, amount: float):
        pass

    def update_realized_pnl(self, amount: float):
        pass

