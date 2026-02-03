from fastapi import APIRouter, HTTPException

from prices.models import price_store
from prices.schemas import PriceUpdate, PriceResponse, AllPricesResponse

router = APIRouter(prefix="/prices", tags=["prices"])


@router.post("/{symbol}", response_model=PriceResponse)
def update_price(symbol: str, price_update: PriceUpdate) -> PriceResponse:
    """Update the price store with the user provided price.

    Mimics incoming price feed.
    """
    price = price_store.update_price(symbol, price_update.price)
    return PriceResponse(
        symbol=price.symbol,
        price=price.price,
        timestamp=price.timestamp
    )


@router.get("", response_model=AllPricesResponse)
def get_all_prices() -> AllPricesResponse:
    """Get all current prices."""
    prices = price_store.get_all_prices()
    return AllPricesResponse(
        prices={
            symbol: PriceResponse(
                symbol=p.symbol,
                price=p.price,
                timestamp=p.timestamp
            )
            for symbol, p in prices.items()
        }
    )


@router.get("/{symbol}", response_model=PriceResponse)
def get_price(symbol: str) -> PriceResponse:
    """Get the price of the given symbol."""
    price = price_store.get_price(symbol)
    if price is None:
        raise HTTPException(status_code=404, detail=f"Price not found for symbol: {symbol}")
    return PriceResponse(
        symbol=price.symbol,
        price=price.price,
        timestamp=price.timestamp
    )
