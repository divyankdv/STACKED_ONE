"""
============================================================

                    STACKED ONE

               EXHAUSTION ENGINE

------------------------------------------------------------

Composite Analytics Engine

Consumes CompositeAnalyticsContext.

Determines whether buyers or sellers are becoming
exhausted.

============================================================
"""

from __future__ import annotations

from app.analytics.base_composite_engine import CompositeAnalyticsEngine
from app.analytics.exhaustion_snapshot import ExhaustionSnapshot
from app.config.settings import settings


class ExhaustionEngine(CompositeAnalyticsEngine):

    snapshot_name = "exhaustion"

    dependencies = [

        "liquidity",

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

        self.buyer_exhausted = False

        self.seller_exhausted = False

        self.dominant_side = "none"

        self.confidence = 0.0

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

        buyer_score = 0.0

        seller_score = 0.0

        #
        # Buyer aggression
        #

        if (

            analytics.order_flow.buy_aggression

            >= settings.exhaustion_buy_aggression

        ):

            buyer_score += 35

        #
        # Seller aggression
        #

        if (

            analytics.order_flow.sell_aggression

            >= settings.exhaustion_sell_aggression

        ):

            seller_score += 35

        #
        # CVD
        #

        if analytics.cvd.current > settings.exhaustion_cvd_threshold:

            buyer_score += 25

        elif analytics.cvd.current < -settings.exhaustion_cvd_threshold:

            seller_score += 25

        #
        # Liquidity
        #

        if (

            liquidity.score

            >= settings.exhaustion_liquidity_threshold

        ):

            buyer_score += 40

            seller_score += 40

        #
        # Final Decision
        #

        if buyer_score >= 80:

            self.buyer_exhausted = True

            self.dominant_side = "buyers"

            self.confidence = buyer_score / 100

        elif seller_score >= 80:

            self.seller_exhausted = True

            self.dominant_side = "sellers"

            self.confidence = seller_score / 100

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return ExhaustionSnapshot(

            buyer_exhausted=self.buyer_exhausted,

            seller_exhausted=self.seller_exhausted,

            confidence=self.confidence,

            dominant_side=self.dominant_side,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "ExhaustionEngine("

            f"buyer={self.buyer_exhausted}, "

            f"seller={self.seller_exhausted}, "

            f"confidence={self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__