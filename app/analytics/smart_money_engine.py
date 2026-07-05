"""
============================================================

                    STACKED ONE

               SMART MONEY ENGINE

------------------------------------------------------------

Composite Analytics Engine

Orchestrates Smart Money analysis.

============================================================
"""

from __future__ import annotations

from app.analytics.base_composite_engine import (
    CompositeAnalyticsEngine,
)
from app.analytics.smart_money.bias_calculator import (
    BiasCalculator,
)
from app.analytics.smart_money.evidence_builder import (
    EvidenceBuilder,
)
from app.analytics.smart_money.pattern_library import (
    PatternLibrary,
)
from app.analytics.smart_money.score_calculator import (
    ScoreCalculator,
)
from app.analytics.smart_money_bias import (
    SmartMoneyBias,
)
from app.analytics.smart_money_snapshot import (
    SmartMoneySnapshot,
)


class SmartMoneyEngine(CompositeAnalyticsEngine):

    snapshot_name = "smart_money"

    dependencies = [

        "liquidity",

        "exhaustion",

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

        self.bias = SmartMoneyBias.NEUTRAL

        self.accumulating = False

        self.distributing = False

        self.institutional_score = 0.0

        self.confidence = 0.0

        self.evidence = ()

    # =====================================================
    # Update
    # =====================================================

    def update(

        self,

        context,

    ):

        self.reset()

        #
        # Build base evidence
        #

        evidence = EvidenceBuilder.build(

            context,

        )

        #
        # Apply institutional patterns
        #

        PatternLibrary.apply(

            context,

            evidence,

        )

        #
        # Calculate score
        #

        score, confidence = ScoreCalculator.calculate(

            evidence,

        )

        #
        # Determine bias
        #

        bias = BiasCalculator.calculate(

            evidence,

            score,

        )

        #
        # Store results
        #

        self.bias = bias

        self.institutional_score = score

        self.confidence = confidence

        self.accumulating = (

            bias == SmartMoneyBias.LONG

        )

        self.distributing = (

            bias == SmartMoneyBias.SHORT

        )

        self.evidence = evidence.to_tuple()

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return SmartMoneySnapshot(

            bias=self.bias,

            accumulating=self.accumulating,

            distributing=self.distributing,

            institutional_score=self.institutional_score,

            confidence=self.confidence,

            evidence=self.evidence,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "SmartMoneyEngine("

            f"bias={self.bias.value}, "

            f"score={self.institutional_score:.1f}, "

            f"confidence={self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__