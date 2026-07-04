"""
============================================================

                    STACKED ONE

                DECISION POLICY

------------------------------------------------------------

Centralized decision logic used by every strategy.

Converts confidence and directional votes into a
SignalSide.

============================================================
"""

from __future__ import annotations

from app.config.settings import settings
from app.strategy.signal_side import SignalSide


class DecisionPolicy:
    """
    Shared signal decision policy.
    """

    # =====================================================
    # Decide
    # =====================================================

    @staticmethod
    def decide(

        confidence: float,

        bullish_votes: int,

        bearish_votes: int,

    ) -> SignalSide:

        #
        # Confidence filter
        #

        if confidence < settings.strategy_signal_threshold:

            return SignalSide.NEUTRAL

        #
        # Minimum directional advantage
        #

        vote_margin = 1

        #
        # BUY
        #

        if bullish_votes >= bearish_votes + vote_margin:

            return SignalSide.BUY

        #
        # SELL
        #

        if bearish_votes >= bullish_votes + vote_margin:

            return SignalSide.SELL

        #
        # Otherwise
        #

        return SignalSide.NEUTRAL

    # =====================================================
    # Consensus Strength
    # =====================================================

    @staticmethod
    def consensus(

        bullish_votes: int,

        bearish_votes: int,

    ) -> float:

        total = bullish_votes + bearish_votes

        if total == 0:

            return 0.0

        return abs(

            bullish_votes - bearish_votes

        ) / total