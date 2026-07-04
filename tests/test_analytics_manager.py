"""
============================================================

        TEST ANALYTICS MANAGER

============================================================
"""

from app.analytics.analytics_manager import AnalyticsManager
from app.exchange.protocol.trade_message import TradeMessage


def make_trade(side, price, size):

    if side == "buy":
        buyer = "taker"
        seller = "maker"
    else:
        buyer = "maker"
        seller = "taker"

    return TradeMessage.from_delta(

        {
            "symbol": "BTCUSD",
            "product_id": 27,
            "price": price,
            "size": size,
            "buyer_role": buyer,
            "seller_role": seller,
            "timestamp": 1782918453777950,
        }

    )


def main():

    analytics = AnalyticsManager()

    analytics.update_trade(make_trade("buy", 100, 10))
    analytics.update_trade(make_trade("sell", 101, 5))
    analytics.update_trade(make_trade("buy", 102, 20))

    snapshot = analytics.snapshot()

    print()
    print("=" * 60)
    print("ANALYTICS SNAPSHOT")
    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    assert snapshot.order_flow.delta == 25

    assert snapshot.cvd.current == 25

    assert snapshot.large_trades.total_large_trades == 0

    assert snapshot.large_trades.largest_trade == 0

    assert snapshot.iceberg.active is False

    assert snapshot.iceberg.confidence == 0.0

    print()

    print("✓ ANALYTICS MANAGER PASSED")


if __name__ == "__main__":

    main()