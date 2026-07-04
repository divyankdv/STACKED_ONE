"""
============================================================

                    STACKED ONE

                 SIGNAL RANKER

============================================================
"""

from __future__ import annotations

from app.strategy.strategy_signal import StrategySignal


class SignalRanker:

    """
    Selects the strongest strategy signal.
    """

    @staticmethod
    def rank(

        signals: tuple[StrategySignal, ...],

    ) -> StrategySignal | None:

        if not signals:

            return None

        return max(

            signals,

            key=lambda signal: (

                signal.confidence,

                signal.score,

            ),

        )