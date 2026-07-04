"""
============================================================

                    STACKED ONE

                LIQUIDITY ENGINE

============================================================
"""

from __future__ import annotations

from app.analytics.base_composite_engine import CompositeAnalyticsEngine
from app.analytics.liquidity_snapshot import LiquiditySnapshot


class LiquidityEngine(CompositeAnalyticsEngine):

    snapshot_name = "liquidity"
    dependencies = []

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.score = 0.0
        self.state = "LOW"

        self.absorption = False
        self.iceberg = False
        self.institutional_activity = False

        self.confidence = 0.0

    # =====================================================
    # Update
    # =====================================================

    def update(self, context):

        analytics = context.analytics

        score = 0.0

        #
        # Absorption
        #

        if analytics.absorption.active:
            self.absorption = True
            score += 40
        else:
            self.absorption = False

        #
        # Iceberg
        #

        if analytics.iceberg.active:
            self.iceberg = True
            score += 30
        else:
            self.iceberg = False

        #
        # Large Trades
        #

        if analytics.large_trades.total_large_trades > 0:
            score += 20

        #
        # Aggression
        #

        aggression = analytics.order_flow.buy_aggression

        if 40 <= aggression <= 60:
            score += 10

        elif 30 <= aggression <= 70:
            score += 5

        self.score = score

        self.institutional_activity = (
            self.absorption
            or self.iceberg
            or analytics.large_trades.total_large_trades > 0
        )

        self.confidence = self.score / 100

        if score >= 80:
            self.state = "HIGH"

        elif score >= 50:
            self.state = "MEDIUM"

        else:
            self.state = "LOW"

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return LiquiditySnapshot(

            score=self.score,

            state=self.state,

            absorption=self.absorption,

            iceberg=self.iceberg,

            institutional_activity=self.institutional_activity,

            confidence=self.confidence,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (
            f"LiquidityEngine(score={self.score:.1f}, "
            f"state={self.state}, "
            f"confidence={self.confidence:.2f})"
        )

    __repr__ = __str__