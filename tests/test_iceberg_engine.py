"""
============================================================

                STACKED ONE

           TEST ICEBERG ENGINE

------------------------------------------------------------

Verifies:

✓ No iceberg before thresholds
✓ Iceberg detection
✓ Correct side detection
✓ Volume accumulation
✓ Trade counting
✓ Confidence calculation

============================================================
"""

from app.analytics.iceberg_engine import IcebergEngine
from app.exchange.protocol.trade_message import TradeMessage


# =====================================================
# Helper
# =====================================================

def make_trade(
    side: str,
    price: float,
    size: float,
):

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


# =====================================================
# Main Test
# =====================================================

def main():

    engine = IcebergEngine(

        volume_threshold=500,

        trade_threshold=4,

    )

    #
    # Same price
    # Heavy selling
    #

    engine.update_trade(
        make_trade("sell", 60000, 120)
    )

    engine.update_trade(
        make_trade("sell", 60000, 150)
    )

    engine.update_trade(
        make_trade("sell", 60000, 180)
    )

    #
    # Threshold not reached yet
    #

    snapshot = engine.snapshot()

    assert snapshot.active is False

    #
    # Fourth trade
    #

    engine.update_trade(
        make_trade("sell", 60000, 160)
    )

    snapshot = engine.snapshot()

    print()

    print("=" * 60)

    print("ICEBERG SNAPSHOT")

    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    print()

    # =====================================================
    # Assertions
    # =====================================================

    assert snapshot.active is True

    assert snapshot.side == "buy"

    assert snapshot.price == 60000

    assert snapshot.trade_count == 4

    assert snapshot.absorbed_volume == 610

    assert snapshot.confidence == 1.0

    print("✓ ICEBERG ENGINE PASSED")


# =====================================================
# Entry
# =====================================================

if __name__ == "__main__":

    main()