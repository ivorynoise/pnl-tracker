from fastapi import APIRouter

from prices.models import Price
from prices.schemas import PriceResponse

router = APIRouter(prefix="/prices", tags=["prices"])


@router.post("/{symbol}")
def update_price(symbol: str):
    # Update the price store with the user provided price
    # mimics incoming price feed
    pass


@router.get("/{symbol}")
def get_price(symbol: str):
    # Gets the price of the given symbol
    pass
