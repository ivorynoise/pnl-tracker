from fastapi import APIRouter

from trades.models import Trade

router = APIRouter(prefix="/trades", tags=["trades"])


@router.post("")
def on_trade(trade: Trade):
    # Update the trade store with the new trade
    # update the position Store accordingly
    pass


@router.get("")
def get_trades():
    # Update the trade store with the new trade
    # update the position Store accordingly
    pass


@router.get("/{symbol}")
def get_symbol_trades(symbol: str):
    pass
