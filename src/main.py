from fastapi import FastAPI

from trades.api import router as trades_router
from position.api import router as position_router
from portfolio.api import router as portfolio_router
from prices.api import router as prices_router

app = FastAPI(
    title="Pnl Tracker API",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

API_V1_PREFIX = "/api/v1"

app.include_router(trades_router, prefix=API_V1_PREFIX)
app.include_router(position_router, prefix=API_V1_PREFIX)
app.include_router(portfolio_router, prefix=API_V1_PREFIX)
app.include_router(prices_router, prefix=API_V1_PREFIX)
