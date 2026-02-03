from fastapi import APIRouter, HTTPException

from position.models import position_store
from position.schemas import PositionResponse, AllPositionsResponse

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/{symbol}", response_model=PositionResponse)
def get_symbol_position(symbol: str) -> PositionResponse:
    """Get position for a specific symbol."""
    position = position_store.get_position(symbol)
    if position is None:
        raise HTTPException(status_code=404, detail=f"Position not found for symbol: {symbol}")
    return PositionResponse(
        symbol=position.symbol,
        quantity=position.quantity,
        avg_price=position.avg_price,
        realized_pnl=position.realized_pnl
    )


@router.get("", response_model=AllPositionsResponse)
def get_all_positions() -> AllPositionsResponse:
    """Get all positions."""
    positions = position_store.get_all_positions()
    return AllPositionsResponse(
        positions={
            symbol: PositionResponse(
                symbol=p.symbol,
                quantity=p.quantity,
                avg_price=p.avg_price,
                realized_pnl=p.realized_pnl
            )
            for symbol, p in positions.items()
        }
    )
