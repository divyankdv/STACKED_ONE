"""
============================================================

                STACKED ONE

           TEST EXHAUSTION ENGINE

============================================================
"""

from app.analytics.absorption_snapshot import AbsorptionSnapshot
from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.analytics.composite_context import CompositeAnalyticsContext
from app.analytics.cvd_snapshot import CVDSnapshot
from app.analytics.exhaustion_engine import ExhaustionEngine
from app.analytics.iceberg_snapshot import IcebergSnapshot
from app.analytics.large_trade_snapshot import LargeTradeSnapshot
from app.analytics.liquidity_snapshot import LiquiditySnapshot
from app.analytics.order_flow_snapshot import OrderFlowSnapshot


def build_context():

    analytics = AnalyticsSnapshot(

        order_flow=OrderFlowSnapshot(

            buy_volume=900,

            sell_volume=100,

            delta=800,

            cvd=800,

            total_volume=1000,

            total_value=60000000,

            vwap=60000,

            trade_count=40,

            buy_trades=35,

            sell_trades=5,

            largest_trade=200,

            buy_aggression=85,

            sell_aggression=15,

        ),

        cvd=CVDSnapshot(

            current=500,

            highest=500,

            lowest=0,

            session_open=0,

            trade_count=40,

        ),

        large_trades=LargeTradeSnapshot(

            total_large_trades=6,

            buy_large_trades=5,

            sell_large_trades=1,

            largest_trade=250,

            average_large_trade=180,

            total_large_volume=950,

        ),

        absorption=AbsorptionSnapshot(

            bullish_score=1.0,

            bearish_score=0.0,

            active=True,

            absorbed_volume=900,

            duration_seconds=60,

            last_price=60000,

        ),

        iceberg=IcebergSnapshot(

            active=True,

            side="buy",

            price=60000,

            absorbed_volume=900,

            trade_count=8,

            confidence=1.0,

        ),

    )

    context = CompositeAnalyticsContext(

        analytics=analytics,

        liquidity=LiquiditySnapshot(

            score=100,

            state="HIGH",

            absorption=True,

            iceberg=True,

            institutional_activity=True,

            confidence=1.0,

        ),

    )

    return context


def main():

    engine = ExhaustionEngine()

    context = build_context()

    engine.update(

        context

    )

    snapshot = engine.snapshot()

    print()

    print("=" * 60)

    print("EXHAUSTION SNAPSHOT")

    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    print()

    #
    # Assertions
    #

    assert snapshot.buyer_exhausted is True

    assert snapshot.seller_exhausted is False

    assert snapshot.dominant_side == "buyers"

    assert snapshot.confidence == 1.0

    print("✓ EXHAUSTION ENGINE PASSED")


if __name__ == "__main__":

    main()