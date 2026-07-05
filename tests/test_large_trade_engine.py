"""
============================================================

                STACKED ONE

          TEST LARGE TRADE ENGINE

------------------------------------------------------------

Verifies:

✓ Small trades are ignored
✓ Large BUY trades are counted
✓ Large SELL trades are counted
✓ Largest trade tracking
✓ Average large trade size
✓ Total large volume

============================================================
"""

from app.analytics.large_trade_engine import LargeTradeEngine
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

    engine = LargeTradeEngine(

        threshold=50

    )

    #
    # Small trades (ignored)
    #

    engine.update_trade(
        make_trade("buy", 60000, 10)
    )

    engine.update_trade(
        make_trade("sell", 60001, 20)
    )

    #
    # Large BUY
    #

    engine.update_trade(
        make_trade("buy", 60002, 75)
    )

    #
    # Large SELL
    #

    engine.update_trade(
        make_trade("sell", 60003, 120)
    )

    #
    # Large BUY
    #

    engine.update_trade(
        make_trade("buy", 60004, 60)
    )

    snapshot = engine.snapshot()

    print()

    print("=" * 60)

    print("LARGE TRADE SNAPSHOT")

    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    print()

    # =====================================================
    # Assertions
    # =====================================================

    assert snapshot.total_large_trades == 3

    assert snapshot.buy_large_trades == 2

    assert snapshot.sell_large_trades == 1

    assert snapshot.largest_trade == 120

    assert snapshot.total_large_volume == 255

    assert snapshot.average_large_trade == 85

    print("✓ LARGE TRADE ENGINE PASSED")


# =====================================================
# Entry
# =====================================================

if __name__ == "__main__":

    main()