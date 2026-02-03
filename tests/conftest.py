import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import app
from trades.models import trade_store
from position.models import position_store
from prices.models import price_store


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_stores():
    """Reset stores before each test."""
    # This is done to showcase the idea; in real scenarios, I will conside more robust state management
    trade_store.trades = []
    position_store.positions = {}
    price_store.prices = {}
    yield
    trade_store.trades = []
    position_store.positions = {}
    price_store.prices = {}
