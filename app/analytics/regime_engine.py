"""
============================================================

                    STACKED ONE

                 REGIME ENGINE

------------------------------------------------------------

Composite Analytics Engine

Infers the current market regime from
multiple composite analytics.

============================================================
"""

from __future__ import annotations

from app.analytics.base_composite_engine import (
    CompositeAnalyticsEngine,
)

from app.analytics.regime_snapshot import (
    RegimeSnapshot,
)

from app.analytics.market_regime import (
    MarketRegime,
)

from app.analytics.evidence import (
    Evidence,
)

from app.analytics.evidence_collection import (
    EvidenceCollection,
)


class RegimeEngine(CompositeAnalyticsEngine):

    snapshot_name = "regime"

    dependencies = [

        "liquidity",

        "exhaustion",

        "smart_money",

    ]

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.regime = MarketRegime.UNKNOWN

        self.strength = 0.0

        self.confidence = 0.0

        self.participation = "LOW"

        self.evidence = ()

    # =====================================================
    # Update
    # =====================================================

    def update(

        self,

        context,

    ):

        self.reset()

        analytics = context.analytics

        liquidity = context.liquidity

        exhaustion = context.exhaustion

        smart = context.smart_money

        evidence = EvidenceCollection()

        #
        # Participation
        #

        if liquidity.institutional_activity:

            evidence.add(

                Evidence(

                    category="Liquidity",

                    description="Institutional liquidity",

                    weight=25,

                    bullish=True,

                )

            )

            self.participation = "HIGH"

        #
        # Trend Direction
        #

        if smart.bias == "LONG":

            evidence.add(

                Evidence(

                    category="Smart Money",

                    description="Institutional accumulation",

                    weight=25,

                    bullish=True,

                )

            )

        elif smart.bias == "SHORT":

            evidence.add(

                Evidence(

                    category="Smart Money",

                    description="Institutional distribution",

                    weight=25,

                    bullish=False,

                )

            )

        #
        # Exhaustion
        #

        if exhaustion.seller_exhausted:

            evidence.add(

                Evidence(

                    category="Exhaustion",

                    description="Seller exhaustion",

                    weight=20,

                    bullish=True,

                )

            )

        elif exhaustion.buyer_exhausted:

            evidence.add(

                Evidence(

                    category="Exhaustion",

                    description="Buyer exhaustion",

                    weight=20,

                    bullish=False,

                )

            )

        #
        # CVD Confirmation
        #

        if analytics.cvd.current > 0:

            evidence.add(

                Evidence(

                    category="CVD",

                    description="Positive CVD",

                    weight=15,

                    bullish=True,

                )

            )

        elif analytics.cvd.current < 0:

            evidence.add(

                Evidence(

                    category="CVD",

                    description="Negative CVD",

                    weight=15,

                    bullish=False,

                )

            )

        #
        # Score
        #

        total = evidence.total_weight

        bullish = evidence.bullish_weight

        bearish = evidence.bearish_weight

        self.strength = total / 100

        self.confidence = min(

            total / 100,

            1.0,

        )

        #
        # Regime
        #

        if total >= 70:

            if bullish > bearish:

                if exhaustion.seller_exhausted:

                    self.regime = MarketRegime.ACCUMULATION

                else:

                    self.regime = MarketRegime.TREND_UP

            else:

                if exhaustion.buyer_exhausted:

                    self.regime = MarketRegime.DISTRIBUTION

                else:

                    self.regime = MarketRegime.TREND_DOWN

        elif total >= 40:

            self.regime = MarketRegime.RANGE

        else:

            self.regime = MarketRegime.UNKNOWN

        self.evidence = evidence.to_tuple()

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return RegimeSnapshot(

            regime=self.regime,

            strength=self.strength,

            confidence=self.confidence,

            participation=self.participation,

            evidence=self.evidence,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "RegimeEngine("

            f"regime={self.regime.value}, "

            f"strength={self.strength:.2f}, "

            f"confidence={self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__