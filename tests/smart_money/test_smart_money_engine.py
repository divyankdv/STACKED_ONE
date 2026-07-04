"""
============================================================

                STACKED ONE

          TEST SMART MONEY ENGINE

------------------------------------------------------------

Tests the complete Smart Money pipeline.

Evidence Builder
        ↓
Pattern Library
        ↓
Score Calculator
        ↓
Bias Calculator
        ↓
SmartMoneyEngine

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

from app.analytics.smart_money_engine import SmartMoneyEngine
from app.analytics.smart_money_bias import SmartMoneyBias


# =====================================================
# Build Context
# =====================================================

def build_context():

    analytics = AnalyticsSnapshot(

        order_flow=OrderFlowSnapshot(

            buy_volume=1800,
            sell_volume=100,
            delta=1700,
            cvd=1700,
            total_volume=1900,
            total_value=190000,
            vwap=100,
            trade_count=35,
            buy_trades=31,
            sell_trades=4,
            largest_trade=350,
            buy_aggression=95,
            sell_aggression=5,

        ),

        cvd=CVDSnapshot(

            current=1700,
            highest=1700,
            lowest=0,
            session_open=0,
            trade_count=35,

        ),

        large_trades=LargeTradeSnapshot(

            total_large_trades=6,
            buy_large_trades=6,
            sell_large_trades=0,
            largest_trade=350,
            average_large_trade=240,
            total_large_volume=1440,

        ),

        absorption=AbsorptionSnapshot(

            bullish_score=1.0,
            bearish_score=0.0,
            active=True,
            absorbed_volume=1400,
            duration_seconds=45,
            last_price=100,

        ),

        iceberg=IcebergSnapshot(

            active=True,
            side="buy",
            price=100,
            absorbed_volume=1200,
            trade_count=7,
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


# =====================================================
# Main
# =====================================================

def main():

    context = build_context()

    engine = SmartMoneyEngine()

    engine.update(

        context,

    )

    snapshot = engine.snapshot()

    print()

    print("=" * 60)

    print("SMART MONEY SNAPSHOT")

    print("=" * 60)

    print(snapshot)

    print("=" * 60)

    print()

    #
    # Assertions
    #

    assert snapshot.bias == SmartMoneyBias.LONG

    assert snapshot.accumulating is True

    assert snapshot.distributing is False

    assert snapshot.institutional_score > 0

    assert 0 <= snapshot.confidence <= 1

    assert len(snapshot.evidence) > 0

    #
    # Evidence sanity
    #

    bullish = [

        e

        for e in snapshot.evidence

        if e.bullish

    ]

    assert len(bullish) > 0

    print("✓ SMART MONEY ENGINE PASSED")


if __name__ == "__main__":

    main()