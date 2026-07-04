"""
============================================================

                STACKED ONE

        TEST EVIDENCE BUILDER

============================================================
"""

from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.analytics.order_flow_snapshot import OrderFlowSnapshot
from app.analytics.cvd_snapshot import CVDSnapshot
from app.analytics.large_trade_snapshot import LargeTradeSnapshot
from app.analytics.absorption_snapshot import AbsorptionSnapshot
from app.analytics.iceberg_snapshot import IcebergSnapshot

from app.analytics.liquidity_snapshot import LiquiditySnapshot
from app.analytics.exhaustion_snapshot import ExhaustionSnapshot

from app.analytics.composite_context import CompositeAnalyticsContext

from app.analytics.smart_money.evidence_builder import (
    EvidenceBuilder,
)


def build_context():

    analytics = AnalyticsSnapshot(

        order_flow=OrderFlowSnapshot(

            buy_volume=1000,
            sell_volume=100,
            delta=900,
            cvd=900,
            total_volume=1100,
            total_value=110000,
            vwap=100,
            trade_count=20,
            buy_trades=18,
            sell_trades=2,
            largest_trade=250,
            buy_aggression=90,
            sell_aggression=10,

        ),

        cvd=CVDSnapshot(

            current=900,
            highest=900,
            lowest=0,
            session_open=0,
            trade_count=20,

        ),

        large_trades=LargeTradeSnapshot(

            total_large_trades=5,
            buy_large_trades=5,
            sell_large_trades=0,
            largest_trade=250,
            average_large_trade=180,
            total_large_volume=900,

        ),

        absorption=AbsorptionSnapshot(

            bullish_score=1.0,
            bearish_score=0.0,
            active=True,
            absorbed_volume=900,
            duration_seconds=30,
            last_price=100,

        ),

        iceberg=IcebergSnapshot(

            active=True,
            side="buy",
            price=100,
            absorbed_volume=900,
            trade_count=5,
            confidence=1.0,

        ),

    )

    return CompositeAnalyticsContext(

        analytics=analytics,

        liquidity=LiquiditySnapshot(

            score=90,
            state="HIGH",
            absorption=True,
            iceberg=True,
            institutional_activity=True,
            confidence=0.9,

        ),

        exhaustion=ExhaustionSnapshot(

            buyer_exhausted=False,
            seller_exhausted=True,
            confidence=0.8,
            dominant_side="SELLERS",

        ),

    )


def main():

    context = build_context()

    evidence = EvidenceBuilder.build(

        context,

    )

    print()

    print("=" * 60)

    print("EVIDENCE")

    print("=" * 60)

    for item in evidence.items:

        print(item)

    print("=" * 60)

    print()

    #
    # Assertions
    #

    assert len(evidence.items) > 0

    assert evidence.total_weight > 0

    assert evidence.bullish_weight > 0

    assert evidence.bearish_weight >= 0

    print("✓ EVIDENCE BUILDER PASSED")


if __name__ == "__main__":

    main()