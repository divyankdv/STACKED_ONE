"""
============================================================

                STACKED ONE

     TEST COMPOSITE ANALYTICS MANAGER

------------------------------------------------------------

Verifies

✓ CompositeAnalyticsManager
✓ LiquidityEngine execution
✓ ExhaustionEngine execution
✓ Context population

============================================================
"""

from app.analytics.absorption_snapshot import (
    AbsorptionSnapshot,
)
from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.analytics.composite_analytics_manager import (
    CompositeAnalyticsManager,
)
from app.analytics.cvd_snapshot import (
    CVDSnapshot,
)
from app.analytics.iceberg_snapshot import (
    IcebergSnapshot,
)
from app.analytics.large_trade_snapshot import (
    LargeTradeSnapshot,
)
from app.analytics.order_flow_snapshot import (
    OrderFlowSnapshot,
)

# =====================================================
# Build Analytics Snapshot
# =====================================================

def build_snapshot():

    return AnalyticsSnapshot(

        order_flow=OrderFlowSnapshot(

            buy_volume=100,

            sell_volume=100,

            delta=0,

            cvd=0,

            total_volume=200,

            total_value=12000000,

            vwap=60000,

            trade_count=20,

            buy_trades=10,

            sell_trades=10,

            largest_trade=120,

            buy_aggression=50,

            sell_aggression=50,

        ),

        cvd=CVDSnapshot(

            current=0,

            highest=50,

            lowest=-50,

            session_open=0,

            trade_count=20,

        ),

        large_trades=LargeTradeSnapshot(

            total_large_trades=5,

            buy_large_trades=3,

            sell_large_trades=2,

            largest_trade=250,

            average_large_trade=180,

            total_large_volume=900,

        ),

        absorption=AbsorptionSnapshot(

            bullish_score=1.0,

            bearish_score=0.0,

            active=True,

            absorbed_volume=900,

            duration_seconds=45,

            last_price=60000,

        ),

        iceberg=IcebergSnapshot(

            active=True,

            side="buy",

            price=60000,

            absorbed_volume=900,

            trade_count=6,

            confidence=1.0,

        ),

    )


# =====================================================
# Main Test
# =====================================================

def main():

    manager = CompositeAnalyticsManager()

    context = manager.update(

        build_snapshot()

    )

    print()

    print("=" * 60)

    print("COMPOSITE CONTEXT")

    print("=" * 60)

    print(context)

    print("=" * 60)

    print()

    # =====================================================
    # Liquidity Assertions
    # =====================================================

    assert context.liquidity is not None

    assert context.liquidity.score == 100

    assert context.liquidity.state == "HIGH"

    assert context.liquidity.absorption is True

    assert context.liquidity.iceberg is True

    assert context.liquidity.institutional_activity is True

    assert context.liquidity.confidence == 1.0

    # =====================================================
    # Exhaustion Assertions
    #
    # Balanced market
    # No exhaustion expected
    # =====================================================

    assert context.exhaustion is not None

    assert context.exhaustion.buyer_exhausted is False

    assert context.exhaustion.seller_exhausted is False

    assert context.exhaustion.dominant_side == "none"

    assert context.exhaustion.confidence == 0.0

    print("✓ COMPOSITE ANALYTICS MANAGER PASSED")


# =====================================================
# Entry
# =====================================================

if __name__ == "__main__":

    main()