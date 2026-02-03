from decimal import Decimal

import pytest


class TestTradesAPI:
    """Test cases for trades API endpoints."""

    def test_create_trade_invalid_side(self, client):
        """Test that invalid side value is rejected."""
        response = client.post(
            "/api/v1/trades",
            json={
                "id": "trade-003",
                "symbol": "BTCUSD",
                "side": "LONG",  # Invalid - should be 'buy' or 'sell'
                "price": "41000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        assert response.status_code == 422  # Validation error


    def test_decimal_precision(self, client):
        """Test that decimal precision is maintained."""
        response = client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000.123456789",
                "quantity": "0.123456789",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        assert response.status_code == 200
        data = response.json()
        # Decimal values should preserve precision
        assert "123456789" in data["price"]
        assert "123456789" in data["quantity"]
