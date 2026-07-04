"""
============================================================

            TEST ABSORPTION ENGINE

============================================================
"""

from app.analytics.absorption_engine import AbsorptionEngine
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

    engine = AbsorptionEngine(

        window_size=5,

        volume_threshold=20,

        price_tolerance=1.0,

    )

    #
    # Heavy selling
    # Price barely moves
    #

    engine.update_trade(make_trade("sell", 100.0, 8))

    engine.update_trade(make_trade("sell", 99.8, 7))

    engine.update_trade(make_trade("sell", 100.1, 9))

    snapshot = engine.snapshot()

    print()

    print("=" * 60)

    print("ABSORPTION SNAPSHOT")

    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    print()

    #
    # Assertions
    #

    assert snapshot.active is True

    assert snapshot.bullish_score > 0

    assert snapshot.bearish_score == 0

    assert snapshot.absorbed_volume == 24

    print("✓ ABSORPTION ENGINE PASSED")


if __name__ == "__main__":

    main()