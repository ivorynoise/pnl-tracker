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

app.include_router(trades_router)
app.include_router(position_router)
app.include_router(portfolio_router)
app.include_router(prices_router)
