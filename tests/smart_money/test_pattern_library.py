"""
============================================================

                STACKED ONE

          TEST PATTERN LIBRARY

============================================================
"""

from app.analytics.absorption_snapshot import AbsorptionSnapshot
from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.analytics.composite_context import CompositeAnalyticsContext
from app.analytics.cvd_snapshot import CVDSnapshot
from app.analytics.exhaustion_snapshot import ExhaustionSnapshot
from app.analytics.iceberg_snapshot import IcebergSnapshot
from app.analytics.large_trade_snapshot import LargeTradeSnapshot
from app.analytics.liquidity_snapshot import LiquiditySnapshot
from app.analytics.order_flow_snapshot import OrderFlowSnapshot
from app.analytics.smart_money.evidence_builder import (
    EvidenceBuilder,
)
from app.analytics.smart_money.pattern_library import (
    PatternLibrary,
)

# =====================================================
# Test Context
# =====================================================

def build_context():

    analytics = AnalyticsSnapshot(

        order_flow=OrderFlowSnapshot(

            buy_volume=1500,
            sell_volume=100,
            delta=1400,
            cvd=1400,
            total_volume=1600,
            total_value=160000,
            vwap=100,
            trade_count=30,
            buy_trades=26,
            sell_trades=4,
            largest_trade=300,
            buy_aggression=94,
            sell_aggression=6,

        ),

        cvd=CVDSnapshot(

            current=1400,
            highest=1400,
            lowest=0,
            session_open=0,
            trade_count=30,

        ),

        large_trades=LargeTradeSnapshot(

            total_large_trades=6,
            buy_large_trades=6,
            sell_large_trades=0,
            largest_trade=300,
            average_large_trade=220,
            total_large_volume=1320,

        ),

        absorption=AbsorptionSnapshot(

            bullish_score=1.0,
            bearish_score=0.0,
            active=True,
            absorbed_volume=1200,
            duration_seconds=35,
            last_price=100,

        ),

        iceberg=IcebergSnapshot(

            active=True,
            side="buy",
            price=100,
            absorbed_volume=1200,
            trade_count=8,
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
            confidence=0.90,

        ),

        exhaustion=ExhaustionSnapshot(

            buyer_exhausted=False,
            seller_exhausted=True,
            confidence=0.80,
            dominant_side="SELLERS",

        ),

    )


# =====================================================
# Main
# =====================================================

def main():

    context = build_context()

    #
    # Base evidence
    #

    evidence = EvidenceBuilder.build(

        context,

    )

    base_count = len(

        evidence.items

    )

    #
    # Apply institutional patterns
    #

    PatternLibrary.apply(

        context,

        evidence,

    )

    print()

    print("=" * 60)

    print("PATTERN LIBRARY")

    print("=" * 60)

    print()

    print(f"Base Evidence     : {base_count}")

    print(f"Final Evidence    : {len(evidence.items)}")

    print(f"Total Weight      : {evidence.total_weight}")

    print(f"Bullish Weight    : {evidence.bullish_weight}")

    print(f"Bearish Weight    : {evidence.bearish_weight}")

    print()

    print("Detected Evidence")

    print("-" * 60)

    for item in evidence.items:

        print(item)

    print("=" * 60)

    print()

    #
    # Assertions
    #

    assert len(evidence.items) >= base_count

    assert evidence.total_weight > 0

    #
    # At least one Pattern evidence
    #

    patterns = [

        item

        for item in evidence.items

        if item.category == "Pattern"

    ]

    assert len(patterns) > 0

    #
    # Institutional accumulation expected
    #

    descriptions = [

        p.description

        for p in patterns

    ]

    assert "Institutional accumulation" in descriptions

    print("✓ PATTERN LIBRARY PASSED")


if __name__ == "__main__":

    main()