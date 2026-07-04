"""
============================================================

            TEST CVD ENGINE

============================================================
"""

from app.analytics.cvd_engine import CVDEngine
from app.exchange.protocol.trade_message import TradeMessage


def make_trade(side: str, price: float, size: float):

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

    engine = CVDEngine()

    engine.update_trade(make_trade("buy", 100, 10))
    engine.update_trade(make_trade("buy", 101, 20))
    engine.update_trade(make_trade("sell", 102, 15))
    engine.update_trade(make_trade("sell", 103, 5))

    snapshot = engine.snapshot()

    print()
    print("=" * 60)
    print("CVD SNAPSHOT")
    print("=" * 60)
    print(snapshot)
    print("=" * 60)
    print()

    assert snapshot.current == 10
    assert snapshot.highest == 30
    assert snapshot.lowest == 0
    assert snapshot.trade_count == 4

    print("✓ ALL TESTS PASSED")


if __name__ == "__main__":
    main()