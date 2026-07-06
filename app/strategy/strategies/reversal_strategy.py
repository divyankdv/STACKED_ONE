"""
============================================================

                    STACKED ONE

               REVERSAL STRATEGY

------------------------------------------------------------

Detects exhaustion driven market reversals.

============================================================
"""

from __future__ import annotations

from app.config.settings import settings
from app.strategy.base_strategy import BaseStrategy
from app.strategy.confidence_builder import ConfidenceBuilder
from app.strategy.decision_policy import DecisionPolicy
from app.strategy.strategy_metadata import StrategyMetadata
from app.strategy.strategy_signal import StrategySignal
from app.strategy.vote_builder import VoteBuilder


class ReversalStrategy(BaseStrategy):
    metadata = StrategyMetadata(
        name="Reversal",
        description="Detects exhaustion driven reversals.",
        category="Mean Reversion",
        timeframe="Any",
        version="1.0",
    )

    # =====================================================

    def evaluate(
        self,
        context,
    ) -> StrategySignal:

        analytics = context.analytics

        confidence = ConfidenceBuilder()

        votes = VoteBuilder()

        #
        # Buyer Exhaustion
        #

        confidence.add(
            context.exhaustion.buyer_exhausted,
            settings.reversal_exhaustion_weight,
            "Buyer Exhaustion",
        )

        votes.bearish(
            context.exhaustion.buyer_exhausted,
            "Buyer Exhaustion",
        )

        #
        # Seller Exhaustion
        #

        confidence.add(
            context.exhaustion.seller_exhausted,
            settings.reversal_exhaustion_weight,
            "Seller Exhaustion",
        )

        votes.bullish(
            context.exhaustion.seller_exhausted,
            "Seller Exhaustion",
        )

        #
        # Bullish Absorption
        #

        confidence.add(
            analytics.absorption.active
            and analytics.absorption.bullish_score > analytics.absorption.bearish_score,
            settings.reversal_absorption_weight,
            "Bullish Absorption",
        )

        votes.bullish(
            analytics.absorption.active
            and analytics.absorption.bullish_score > analytics.absorption.bearish_score,
            "Bullish Absorption",
        )

        #
        # Bearish Absorption
        #

        confidence.add(
            analytics.absorption.active
            and analytics.absorption.bearish_score > analytics.absorption.bullish_score,
            settings.reversal_absorption_weight,
            "Bearish Absorption",
        )

        votes.bearish(
            analytics.absorption.active
            and analytics.absorption.bearish_score > analytics.absorption.bullish_score,
            "Bearish Absorption",
        )

        #
        # Positive CVD
        #

        confidence.add(
            analytics.cvd.current > 0,
            settings.reversal_cvd_weight,
            "Positive CVD",
        )

        votes.bullish(
            analytics.cvd.current > 0,
            "Positive CVD",
        )

        #
        # Negative CVD
        #

        confidence.add(
            analytics.cvd.current < 0,
            settings.reversal_cvd_weight,
            "Negative CVD",
        )

        votes.bearish(
            analytics.cvd.current < 0,
            "Negative CVD",
        )

        #
        # Opposing Evidence
        #

        confidence.add_negative(
            context.smart_money.accumulating,
            0.15,
            "Accumulation",
        )

        confidence.add_negative(
            context.smart_money.distributing,
            0.15,
            "Distribution",
        )

        #
        # Decision
        #

        side = DecisionPolicy.decide(
            confidence=confidence.confidence,
            bullish_votes=votes.bullish_votes,
            bearish_votes=votes.bearish_votes,
        )

        #
        # Return
        #

        return StrategySignal(
            strategy=self.name,
            side=side,
            confidence=confidence.confidence,
            score=confidence.score,
            reasons=confidence.reasons + votes.all_reasons,
        )
