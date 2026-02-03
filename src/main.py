from fastapi import FastAPI

from trades.api import router as trades_router
from position.api import router as position_router
from portfolio.api import router as portfolio_router
from prices.api import router as prices_router

from trades.models import trade_store
from position.models import position_store
from prices.models import price_store

app = FastAPI(
    title="Pnl Tracker API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/clear")
def clear_data_stores():
    """Health check endpoint."""
    trade_store.trades = []
    position_store.positions = {}
    price_store.prices = {}
    return {"status": "data stores cleared"}

API_V1_PREFIX = "/api/v1"

app.include_router(trades_router, prefix=API_V1_PREFIX)
app.include_router(position_router, prefix=API_V1_PREFIX)
app.include_router(portfolio_router, prefix=API_V1_PREFIX)
app.include_router(prices_router, prefix=API_V1_PREFIX)
