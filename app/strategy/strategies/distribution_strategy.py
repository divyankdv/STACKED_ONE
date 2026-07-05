"""
============================================================

                    STACKED ONE

            DISTRIBUTION STRATEGY

------------------------------------------------------------

Detects institutional distribution using composite
analytics.

============================================================
"""

from __future__ import annotations

from app.analytics.market_regime import MarketRegime
from app.config.settings import settings
from app.strategy.base_strategy import BaseStrategy
from app.strategy.confidence_builder import ConfidenceBuilder
from app.strategy.signal_side import SignalSide
from app.strategy.strategy_metadata import StrategyMetadata
from app.strategy.strategy_signal import StrategySignal


class DistributionStrategy(BaseStrategy):

    metadata = StrategyMetadata(

        name="Distribution",

        description="Detects institutional distribution.",

        category="Institutional",

        timeframe="Any",

        version="1.0",

    )

    # =====================================================
    # Evaluate
    # =====================================================

    def evaluate(

        self,

        context,

    ) -> StrategySignal:

        builder = ConfidenceBuilder()

        #
        # -------------------------------------------------
        # High Liquidity
        # -------------------------------------------------
        #

        builder.add(

            context.liquidity.state == "HIGH",

            settings.distribution_liquidity_weight,

            "High liquidity",

        )

        #
        # -------------------------------------------------
        # Smart Money
        # -------------------------------------------------
        #

        builder.add(

            context.smart_money.distributing,

            settings.distribution_smart_money_weight,

            "Institutional distribution",

        )

        #
        # -------------------------------------------------
        # Regime
        # -------------------------------------------------
        #

        builder.add(

            context.regime.regime == MarketRegime.DISTRIBUTION,

            settings.distribution_regime_weight,

            "Distribution regime",

        )

        #
        # -------------------------------------------------
        # Negative CVD
        # -------------------------------------------------
        #

        builder.add(

            context.analytics.cvd.current < 0,

            settings.distribution_cvd_weight,

            "Negative CVD",

        )

        #
        # -------------------------------------------------
        # Opposing Evidence
        # -------------------------------------------------
        #

        builder.add_negative(

            context.smart_money.accumulating,

            0.30,

            "Accumulation detected",

        )

        builder.add_negative(

            context.analytics.cvd.current > 0,

            0.20,

            "Positive CVD",

        )

        #
        # -------------------------------------------------
        # Decision
        # -------------------------------------------------
        #

        if builder.confidence >= settings.strategy_signal_threshold:

            side = SignalSide.SELL

        else:

            side = SignalSide.NEUTRAL

        #
        # -------------------------------------------------
        # Return Signal
        # -------------------------------------------------
        #

        return StrategySignal(

            strategy=self.name,

            side=side,

            confidence=builder.confidence,

            score=builder.score,

            reasons=builder.reasons,

        )