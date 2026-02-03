from fastapi import APIRouter

from trades.models import Trade, trade_store
from trades.schemas import TradeCreate, TradeResponse, TradeListResponse
from position.models import position_store

router = APIRouter(prefix="/trades", tags=["trades"])


@router.post("", response_model=TradeResponse)
def on_trade(trade: TradeCreate) -> TradeResponse:
    """Record a new trade and update position accordingly."""
    trade_obj = Trade(**trade.model_dump())
    trade_store.add_trade(trade_obj)
    position_store.update_position(trade_obj)
    return TradeResponse(**trade_obj.model_dump())


@router.get("", response_model=TradeListResponse)
def get_trades() -> TradeListResponse:
    """Get all trades."""
    trades = trade_store.get_all_trades()
    return TradeListResponse(
        trades=[TradeResponse(**t.model_dump()) for t in trades]
    )


@router.get("/{symbol}", response_model=TradeListResponse)
def get_symbol_trades(symbol: str) -> TradeListResponse:
    """Get all trades for a specific symbol."""
    trades = trade_store.get_trades_by_symbol(symbol)
    return TradeListResponse(
        trades=[TradeResponse(**t.model_dump()) for t in trades]
    )
