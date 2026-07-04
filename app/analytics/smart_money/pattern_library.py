"""
============================================================

                    STACKED ONE

                PATTERN LIBRARY

------------------------------------------------------------

Detects institutional market patterns and contributes
additional evidence.

This module is stateless.

============================================================
"""

from __future__ import annotations

from app.analytics.evidence import Evidence
from app.analytics.evidence_collection import EvidenceCollection
from app.config.settings import settings


class PatternLibrary:

    """
    Detect institutional trading patterns.

    Every detected pattern contributes additional
    Evidence into the EvidenceCollection.
    """

    # =====================================================
    # Public
    # =====================================================

    @staticmethod
    def apply(

        context,

        evidence: EvidenceCollection,

    ) -> None:

        PatternLibrary._institutional_accumulation(

            context,

            evidence,

        )

        PatternLibrary._institutional_distribution(

            context,

            evidence,

        )

        PatternLibrary._hidden_accumulation(

            context,

            evidence,

        )

        PatternLibrary._hidden_distribution(

            context,

            evidence,

        )

        PatternLibrary._aggressive_breakout(

            context,

            evidence,

        )

        PatternLibrary._aggressive_breakdown(

            context,

            evidence,

        )

    # =====================================================
    # Institutional Accumulation
    # =====================================================

    @staticmethod
    def _institutional_accumulation(

        context,

        evidence,

    ):

        analytics = context.analytics

        if (

            analytics.large_trades.buy_large_trades > 0

            and analytics.absorption.active

            and analytics.cvd.current > 0

        ):

            evidence.add(

                Evidence(

                    category="Pattern",

                    description="Institutional accumulation",

                    weight=settings.smart_money_pattern_bonus_weight,

                    bullish=True,

                )

            )

    # =====================================================
    # Institutional Distribution
    # =====================================================

    @staticmethod
    def _institutional_distribution(

        context,

        evidence,

    ):

        analytics = context.analytics

        if (

            analytics.large_trades.sell_large_trades > 0

            and analytics.absorption.active

            and analytics.cvd.current < 0

        ):

            evidence.add(

                Evidence(

                    category="Pattern",

                    description="Institutional distribution",

                    weight=settings.smart_money_pattern_bonus_weight,

                    bullish=False,

                )

            )

    # =====================================================
    # Hidden Accumulation
    # =====================================================

    @staticmethod
    def _hidden_accumulation(

        context,

        evidence,

    ):

        liquidity = context.liquidity

        exhaustion = context.exhaustion

        if (

            liquidity.absorption

            and exhaustion.seller_exhausted

        ):

            evidence.add(

                Evidence(

                    category="Pattern",

                    description="Hidden accumulation",

                    weight=settings.smart_money_hidden_accumulation_weight,

                    bullish=True,

                )

            )

    # =====================================================
    # Hidden Distribution
    # =====================================================

    @staticmethod
    def _hidden_distribution(

        context,

        evidence,

    ):

        liquidity = context.liquidity

        exhaustion = context.exhaustion

        if (

            liquidity.absorption

            and exhaustion.buyer_exhausted

        ):

            evidence.add(

                Evidence(

                    category="Pattern",

                    description="Hidden distribution",

                    weight=settings.smart_money_hidden_distribution_weight,

                    bullish=False,

                )

            )

    # =====================================================
    # Aggressive Breakout
    # =====================================================

    @staticmethod
    def _aggressive_breakout(

        context,

        evidence,

    ):

        analytics = context.analytics

        liquidity = context.liquidity

        if (

            liquidity.state == "HIGH"

            and analytics.iceberg.active

            and analytics.iceberg.side == "buy"

            and analytics.cvd.current > 0

        ):

            evidence.add(

                Evidence(

                    category="Pattern",

                    description="Aggressive breakout",

                    weight=settings.smart_money_pattern_bonus_weight,

                    bullish=True,

                )

            )

    # =====================================================
    # Aggressive Breakdown
    # =====================================================

    @staticmethod
    def _aggressive_breakdown(

        context,

        evidence,

    ):

        analytics = context.analytics

        liquidity = context.liquidity

        if (

            liquidity.state == "HIGH"

            and analytics.iceberg.active

            and analytics.iceberg.side == "sell"

            and analytics.cvd.current < 0

        ):

            evidence.add(

                Evidence(

                    category="Pattern",

                    description="Aggressive breakdown",

                    weight=settings.smart_money_pattern_bonus_weight,

                    bullish=False,

                )

            )