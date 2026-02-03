from fastapi import APIRouter

from portfolio.models import portfolio_service
from portfolio.schemas import PortfolioResponse, PnLResponse, PositionSchema
from position.models import position_store

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=PortfolioResponse)
def get_portfolio() -> PortfolioResponse:
    """Return the current portfolio with all positions and PnL."""
    positions = []
    for symbol, position in position_store.get_all_positions().items():
        unrealized_pnl = portfolio_service.get_position_unrealized_pnl(symbol)
        positions.append(
            PositionSchema(
                symbol=position.symbol,
                quantity=position.quantity,
                avg_price=position.avg_price,
                realized_pnl=position.realized_pnl,
                unrealized_pnl=unrealized_pnl,
            )
        )

    return PortfolioResponse(
        total_unrealized_pnl=portfolio_service.get_total_unrealized_pnl(),
        total_realized_pnl=portfolio_service.get_total_realized_pnl(),
        positions=positions,
    )


@router.get("/pnl", response_model=PnLResponse)
def get_pnl() -> PnLResponse:
    """Return the current unrealized and realized PnL summary."""
    total_unrealized = portfolio_service.get_total_unrealized_pnl()
    total_realized = portfolio_service.get_total_realized_pnl()

    return PnLResponse(
        total_unrealized_pnl=total_unrealized,
        total_realized_pnl=total_realized,
        total_pnl=total_unrealized + total_realized,
    )
