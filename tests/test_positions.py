from decimal import Decimal

import pytest


class TestPositionsAPI:
    """Test cases for positions API endpoints."""

    def test_position_after_single_buy(self, client):
        """Test position after a single buy trade."""
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        assert response.status_code == 200
        data = response.json()
        assert data["symbol"] == "BTCUSD"
        assert Decimal(data["quantity"]) == Decimal("0.3")
        assert Decimal(data["avg_price"]) == Decimal("41000")
        assert Decimal(data["realized_pnl"]) == Decimal("0")
        assert Decimal(data["unrealized_pnl"]) == Decimal("0")  # No price set

    def test_position_average_price_calculation(self, client):
        """Test average price calculation with multiple buys."""
        # Buy 0.3 @ 41000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        # Buy 0.2 @ 42000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "42000",
                "quantity": "0.2",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Total cost = (0.3 * 41000) + (0.2 * 42000) = 12300 + 8400 = 20700
        # Avg price = 20700 / 0.5 = 41400
        assert Decimal(data["quantity"]) == Decimal("0.5")
        assert Decimal(data["avg_price"]) == Decimal("41400")

    def test_position_realized_pnl_on_partial_close(self, client):
        """Test realized PnL when partially closing a position."""
        # Buy 0.5 @ 41000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        # Sell 0.2 @ 42000 (profit)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "42000",
                "quantity": "0.2",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Remaining position: 0.3
        # Realized PnL: 0.2 * (42000 - 41000) = 200
        assert Decimal(data["quantity"]) == Decimal("0.3")
        assert Decimal(data["realized_pnl"]) == Decimal("200")

    def test_position_realized_pnl_loss(self, client):
        """Test realized PnL with a losing trade."""
        # Buy 0.5 @ 42000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "42000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        # Sell 0.5 @ 41000 (loss)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Realized PnL: 0.5 * (41000 - 42000) = -500
        assert Decimal(data["quantity"]) == Decimal("0")
        assert Decimal(data["realized_pnl"]) == Decimal("-500")

    def test_position_short_then_cover(self, client):
        """Test short position and covering."""
        # Sell 0.3 @ 42000 (open short)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "42000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()
        assert Decimal(data["quantity"]) == Decimal("-0.3")  # Short position

        # Buy 0.3 @ 41000 (cover with profit)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Realized PnL: 0.3 * (42000 - 41000) = 300
        assert Decimal(data["quantity"]) == Decimal("0")
        assert Decimal(data["realized_pnl"]) == Decimal("300")

    def test_position_flip_long_to_short(self, client):
        """Test flipping from long to short position."""
        # Buy 0.3 @ 41000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        # Sell 0.5 @ 42000 (close long + open short)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "42000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Closed 0.3 long with PnL: 0.3 * (42000 - 41000) = 300
        # New short position: -0.2 @ 42000
        assert Decimal(data["quantity"]) == Decimal("-0.2")
        assert Decimal(data["avg_price"]) == Decimal("42000")
        assert Decimal(data["realized_pnl"]) == Decimal("300")

    def test_get_all_positions(self, client):
        """Test getting all positions."""
        # Create positions in two symbols
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "ETHUSD",
                "side": "buy",
                "price": "2500",
                "quantity": "1.0",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        response = client.get("/api/v1/positions")
        assert response.status_code == 200
        data = response.json()
        assert "BTCUSD" in data["positions"]
        assert "ETHUSD" in data["positions"]

    def test_position_not_found(self, client):
        """Test getting a position that doesn't exist."""
        response = client.get("/api/v1/positions/UNKNOWN")
        assert response.status_code == 404

    def test_decimal_precision_in_position(self, client):
        """Test that decimal precision is maintained in positions."""
        # Buy 0.3 @ 41000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.3",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        # Buy 0.2 @ 42000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "42000",
                "quantity": "0.2",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )
        # Sell 0.1 @ 42000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-003",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "42000",
                "quantity": "0.1",
                "timestamp": "2026-02-03T16:32:48.534Z",
            },
        )
        # Sell 0.7 @ 41000 (to flip to short)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-004",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "41000",
                "quantity": "0.7",
                "timestamp": "2026-02-03T16:33:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # With Decimal, should be exactly -0.3 not -0.29999999999999993
        assert Decimal(data["quantity"]) == Decimal("-0.3")


class TestUnrealizedPnL:
    """Test cases for unrealized PnL calculations."""

    def test_unrealized_pnl_no_price(self, client):
        """Test unrealized PnL is 0 when no price is set."""
        # Buy position
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # No price set, unrealized PnL should be 0
        assert Decimal(data["unrealized_pnl"]) == Decimal("0")

    def test_unrealized_pnl_long_profit(self, client):
        """Test unrealized PnL for long position in profit."""
        # Buy 0.5 @ 41000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        # Set current price to 43000
        client.post("/api/v1/prices/BTCUSD", json={"price": "43000"})

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Unrealized PnL: 0.5 * (43000 - 41000) = 1000
        assert Decimal(data["unrealized_pnl"]) == Decimal("1000")

    def test_unrealized_pnl_long_loss(self, client):
        """Test unrealized PnL for long position in loss."""
        # Buy 0.5 @ 41000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        # Set current price to 39000
        client.post("/api/v1/prices/BTCUSD", json={"price": "39000"})

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Unrealized PnL: 0.5 * (39000 - 41000) = -1000
        assert Decimal(data["unrealized_pnl"]) == Decimal("-1000")

    def test_unrealized_pnl_short_profit(self, client):
        """Test unrealized PnL for short position in profit."""
        # Sell 0.5 @ 42000 (open short)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "42000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        # Set current price to 40000 (price dropped, short profits)
        client.post("/api/v1/prices/BTCUSD", json={"price": "40000"})

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Unrealized PnL: 0.5 * (42000 - 40000) = 1000
        assert Decimal(data["unrealized_pnl"]) == Decimal("1000")

    def test_unrealized_pnl_short_loss(self, client):
        """Test unrealized PnL for short position in loss."""
        # Sell 0.5 @ 42000 (open short)
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "42000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        # Set current price to 44000 (price went up, short loses)
        client.post("/api/v1/prices/BTCUSD", json={"price": "44000"})

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Unrealized PnL: 0.5 * (42000 - 44000) = -1000
        assert Decimal(data["unrealized_pnl"]) == Decimal("-1000")

    def test_unrealized_pnl_updates_with_price_change(self, client):
        """Test that unrealized PnL updates when price changes."""
        # Buy 0.5 @ 41000
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )

        # Initial price: 42000
        client.post("/api/v1/prices/BTCUSD", json={"price": "42000"})
        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()
        # Unrealized PnL: 0.5 * (42000 - 41000) = 500
        assert Decimal(data["unrealized_pnl"]) == Decimal("500")

        # Price increases to 45000
        client.post("/api/v1/prices/BTCUSD", json={"price": "45000"})
        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()
        # Unrealized PnL: 0.5 * (45000 - 41000) = 2000
        assert Decimal(data["unrealized_pnl"]) == Decimal("2000")

        # Price drops to 38000
        client.post("/api/v1/prices/BTCUSD", json={"price": "38000"})
        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()
        # Unrealized PnL: 0.5 * (38000 - 41000) = -1500
        assert Decimal(data["unrealized_pnl"]) == Decimal("-1500")

    def test_unrealized_pnl_zero_position(self, client):
        """Test unrealized PnL is 0 for closed position."""
        # Buy and then sell same quantity
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "BTCUSD",
                "side": "sell",
                "price": "42000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        # Set a price
        client.post("/api/v1/prices/BTCUSD", json={"price": "45000"})

        response = client.get("/api/v1/positions/BTCUSD")
        data = response.json()

        # Position is 0, unrealized PnL should be 0
        assert Decimal(data["quantity"]) == Decimal("0")
        assert Decimal(data["unrealized_pnl"]) == Decimal("0")
        # But realized PnL should be captured
        assert Decimal(data["realized_pnl"]) == Decimal("500")

    def test_unrealized_pnl_multiple_positions(self, client):
        """Test unrealized PnL for multiple positions."""
        # Buy BTCUSD
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-001",
                "symbol": "BTCUSD",
                "side": "buy",
                "price": "41000",
                "quantity": "0.5",
                "timestamp": "2026-02-03T16:30:48.534Z",
            },
        )
        # Buy ETHUSD
        client.post(
            "/api/v1/trades",
            json={
                "id": "trade-002",
                "symbol": "ETHUSD",
                "side": "buy",
                "price": "2500",
                "quantity": "2.0",
                "timestamp": "2026-02-03T16:31:48.534Z",
            },
        )

        # Set prices
        client.post("/api/v1/prices/BTCUSD", json={"price": "43000"})
        client.post("/api/v1/prices/ETHUSD", json={"price": "2700"})

        response = client.get("/api/v1/positions")
        data = response.json()

        # BTCUSD: 0.5 * (43000 - 41000) = 1000
        assert Decimal(data["positions"]["BTCUSD"]["unrealized_pnl"]) == Decimal("1000")
        # ETHUSD: 2.0 * (2700 - 2500) = 400
        assert Decimal(data["positions"]["ETHUSD"]["unrealized_pnl"]) == Decimal("400")
