"""
============================================================

                STACKED ONE

          TEST LIQUIDITY ENGINE

------------------------------------------------------------

Verifies

✓ Liquidity score
✓ Liquidity state
✓ Institutional activity
✓ Confidence
✓ Composite analytics

============================================================
"""

from app.analytics.analytics_snapshot import AnalyticsSnapshot

from app.analytics.order_flow_snapshot import OrderFlowSnapshot
from app.analytics.cvd_snapshot import CVDSnapshot
from app.analytics.large_trade_snapshot import LargeTradeSnapshot
from app.analytics.absorption_snapshot import AbsorptionSnapshot
from app.analytics.iceberg_snapshot import IcebergSnapshot
from app.analytics.composite_context import CompositeAnalyticsContext

from app.analytics.liquidity_engine import LiquidityEngine


def main():

    #
    # ----------------------------------------------------
    # Fake analytics snapshot
    # ----------------------------------------------------
    #

    analytics = AnalyticsSnapshot(

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

    #
    # ----------------------------------------------------
    # Engine
    # ----------------------------------------------------
    #

    context = CompositeAnalyticsContext(

       analytics=analytics

    )

    engine = LiquidityEngine()

    engine.update(

       context

    )

    snapshot = engine.snapshot()

    print()

    print("=" * 60)

    print("LIQUIDITY SNAPSHOT")

    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    print()

    #
    # ----------------------------------------------------
    # Assertions
    # ----------------------------------------------------
    #

    assert snapshot.score == 100

    assert snapshot.state == "HIGH"

    assert snapshot.absorption is True

    assert snapshot.iceberg is True

    assert snapshot.institutional_activity is True

    assert snapshot.confidence == 1.0

    print("✓ LIQUIDITY ENGINE PASSED")


if __name__ == "__main__":

    main()