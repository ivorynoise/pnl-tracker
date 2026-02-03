from fastapi import APIRouter

from portfolio.models import Portfolio
from portfolio.schemas import PortfolioResponse

router = APIRouter(prefix="/portfolios", tags=["portfolios"])


@router.get("")
def get_portfolio():
    # Return the current portfolio positions
    pass


@router.get("/pnl")
def get_pnl():
    # Return the current unrealized and realized PnL
    pass
