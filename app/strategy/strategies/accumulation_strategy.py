"""
============================================================

                    STACKED ONE

            ACCUMULATION STRATEGY

------------------------------------------------------------

Detects institutional accumulation using composite
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


class AccumulationStrategy(BaseStrategy):

    metadata = StrategyMetadata(

        name="Accumulation",

        description="Detects institutional accumulation.",

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

            settings.accumulation_liquidity_weight,

            "High liquidity",

        )

        #
        # -------------------------------------------------
        # Smart Money
        # -------------------------------------------------
        #

        builder.add(

            context.smart_money.accumulating,

            settings.accumulation_smart_money_weight,

            "Institutional accumulation",

        )

        #
        # -------------------------------------------------
        # Regime
        # -------------------------------------------------
        #

        builder.add(

            context.regime.regime == MarketRegime.ACCUMULATION,

            settings.accumulation_regime_weight,

            "Accumulation regime",

        )

        #
        # -------------------------------------------------
        # Positive CVD
        # -------------------------------------------------
        #

        builder.add(

            context.analytics.cvd.current > 0,

            settings.accumulation_cvd_weight,

            "Positive CVD",

        )

        #
        # -------------------------------------------------
        # Negative Evidence
        # -------------------------------------------------
        #

        builder.add_negative(

            context.smart_money.distributing,

            0.30,

            "Distribution detected",

        )

        builder.add_negative(

            context.analytics.cvd.current < 0,

            0.20,

            "Negative CVD",

        )

        #
        # -------------------------------------------------
        # Decision
        # -------------------------------------------------
        #

        if builder.confidence >= settings.strategy_signal_threshold:

            side = SignalSide.BUY

        else:

            side = SignalSide.NEUTRAL

        #
        # -------------------------------------------------
        # Signal
        # -------------------------------------------------
        #

        return StrategySignal(

            strategy=self.name,

            side=side,

            confidence=builder.confidence,

            score=builder.score,

            reasons=builder.reasons,

        )