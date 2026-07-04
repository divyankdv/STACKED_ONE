"""
============================================================

                    STACKED ONE

               BREAKOUT STRATEGY

------------------------------------------------------------

Detects institutional breakout opportunities using
order flow, liquidity and institutional participation.

============================================================
"""

from __future__ import annotations

from app.config.settings import settings

from app.strategy.base_strategy import BaseStrategy
from app.strategy.strategy_metadata import StrategyMetadata
from app.strategy.strategy_signal import StrategySignal
from app.strategy.signal_side import SignalSide

from app.strategy.confidence_builder import ConfidenceBuilder
from app.strategy.vote_builder import VoteBuilder
from app.strategy.decision_policy import DecisionPolicy


class BreakoutStrategy(BaseStrategy):

    metadata = StrategyMetadata(

        name="Breakout",

        description="Detects institutional breakout.",

        category="Momentum",

        timeframe="Any",

        version="3.0",

    )

    # =====================================================
    # Evaluate
    # =====================================================

    def evaluate(

        self,

        context,

    ) -> StrategySignal:

        analytics = context.analytics

        confidence = ConfidenceBuilder()

        votes = VoteBuilder()

        # =====================================================
        # Liquidity
        # =====================================================

        confidence.add(

            context.liquidity.state == "HIGH",

            settings.breakout_liquidity_weight,

            "High liquidity",

        )

        # =====================================================
        # Iceberg
        # =====================================================

        if analytics.iceberg.active:

            confidence.add(

                True,

                settings.breakout_iceberg_weight,

                "Iceberg detected",

            )

            votes.bullish(

                analytics.iceberg.side == "buy",

                "BUY Iceberg",

            )

            votes.bearish(

                analytics.iceberg.side == "sell",

                "SELL Iceberg",

            )

        # =====================================================
        # Large Trades
        # =====================================================

        if analytics.large_trades.total_large_trades > 0:

            confidence.add(

                True,

                settings.breakout_large_trade_weight,

                "Institutional large trades",

            )

            votes.bullish(

                analytics.large_trades.buy_large_trades >

                analytics.large_trades.sell_large_trades,

                "Buy Large Trades",

            )

            votes.bearish(

                analytics.large_trades.sell_large_trades >

                analytics.large_trades.buy_large_trades,

                "Sell Large Trades",

            )

        # =====================================================
        # CVD
        # =====================================================

        confidence.add(

            analytics.cvd.current > 0,

            settings.breakout_cvd_weight,

            "Positive CVD",

        )

        confidence.add(

            analytics.cvd.current < 0,

            settings.breakout_cvd_weight,

            "Negative CVD",

        )

        votes.bullish(

            analytics.cvd.current > 0,

            "Positive CVD",

        )

        votes.bearish(

            analytics.cvd.current < 0,

            "Negative CVD",

        )

        # =====================================================
        # Aggression
        # =====================================================

        confidence.add(

            analytics.order_flow.buy_aggression >= 70,

            0.10,

            "Strong Buy Aggression",

        )

        confidence.add(

            analytics.order_flow.sell_aggression >= 70,

            0.10,

            "Strong Sell Aggression",

        )

        votes.bullish(

            analytics.order_flow.buy_aggression >= 70,

            "Buy Aggression",

        )

        votes.bearish(

            analytics.order_flow.sell_aggression >= 70,

            "Sell Aggression",

        )

        # =====================================================
        # Exhaustion Filters
        # =====================================================

        confidence.add_negative(

            context.exhaustion.buyer_exhausted,

            0.25,

            "Buyer Exhaustion",

        )

        confidence.add_negative(

            context.exhaustion.seller_exhausted,

            0.25,

            "Seller Exhaustion",

        )

        # =====================================================
        # Final Decision
        # =====================================================

        side = DecisionPolicy.decide(

            confidence=confidence.confidence,

            bullish_votes=votes.bullish_votes,

            bearish_votes=votes.bearish_votes,

        )

        # =====================================================
        # Merge Reasons
        # =====================================================

        reasons = confidence.reasons + votes.all_reasons

        # =====================================================
        # Signal
        # =====================================================

        return StrategySignal(

            strategy=self.name,

            side=side,

            confidence=confidence.confidence,

            score=confidence.score,

            reasons=reasons,

        )