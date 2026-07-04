"""
============================================================

                STACKED ONE

      TEST FULL ANALYTICS PIPELINE

------------------------------------------------------------

End-to-end integration test.

TradeMessage
    ↓
AnalyticsManager
    ↓
AnalyticsSnapshot
    ↓
CompositeAnalyticsManager
    ↓
CompositeAnalyticsContext

============================================================
"""

from datetime import UTC, datetime

from app.analytics.analytics_manager import AnalyticsManager
from app.analytics.composite_analytics_manager import (
    CompositeAnalyticsManager,
)

from app.exchange.protocol.trade_message import TradeMessage
from app.exchange.protocol.order_role import OrderRole


# =====================================================
# Helper
# =====================================================

def trade(

    side: str,

    price: float,

    size: float,

):

    if side == "buy":

        buyer = OrderRole.TAKER

        seller = OrderRole.MAKER

    else:

        buyer = OrderRole.MAKER

        seller = OrderRole.TAKER

    return TradeMessage(

        symbol="BTCUSD",

        product_id=1,

        price=price,

        size=size,

        buyer_role=buyer,

        seller_role=seller,

        timestamp=datetime.now(UTC),

    )


# =====================================================
# Main
# =====================================================

def main():

    analytics = AnalyticsManager()

    composite = CompositeAnalyticsManager()

    #
    # Simulated institutional accumulation
    #

    trades = [

        trade("buy",100,150),

        trade("buy",100.1,180),

        trade("buy",100.2,220),

        trade("buy",100.2,250),

        trade("buy",100.3,300),

        trade("sell",100.3,40),

        trade("buy",100.4,350),

        trade("buy",100.5,400),

    ]

    #
    # Feed analytics
    #

    for t in trades:

        analytics.update_trade(

            t

        )

    #
    # Primary snapshot
    #

    analytics_snapshot = analytics.snapshot()

    #
    # Composite snapshot
    #

    context = composite.update(

        analytics_snapshot

    )

    #
    # Output
    #

    print()

    print("="*60)

    print("PRIMARY")

    print("="*60)

    print(analytics_snapshot)

    print()

    print("="*60)

    print("COMPOSITE")

    print("="*60)

    print(context)

    print()

    #
    # Assertions
    #

    assert context.liquidity is not None

    assert context.exhaustion is not None

    assert context.smart_money is not None

    assert context.regime is not None

    #
    # Smart Money sanity
    #

    assert context.smart_money.institutional_score >= 0

    assert context.smart_money.confidence >= 0

    #
    # Regime sanity
    #

    assert context.regime.confidence >= 0

    print()

    print("✓ FULL PIPELINE PASSED")


if __name__ == "__main__":

    main()