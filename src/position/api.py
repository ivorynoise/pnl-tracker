from fastapi import APIRouter

from position.models import Position
from position.schemas import PositionResponse

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/{symbol}")
def get_symbol_position(symbol: str):
    # Update the price store with the user provided price
    # mimics incoming price feed
    pass


@router.get("")
def get_all_positions():
    pass
