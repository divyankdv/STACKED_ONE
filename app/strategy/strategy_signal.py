"""
============================================================

                    STACKED ONE

                STRATEGY SIGNAL

------------------------------------------------------------

Represents a single trading signal produced by a strategy.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from app.strategy.signal_side import SignalSide


@dataclass(slots=True, frozen=True)
class StrategySignal:
    """
    Output of a trading strategy.
    """

    #
    # Strategy Information
    #

    strategy: str

    #
    # Signal
    #

    side: SignalSide

    #
    # Confidence
    #

    confidence: float

    #
    # Human-readable explanation
    #

    reasons: Tuple[str, ...] = ()

    #
    # Optional metadata
    #

    score: float = 0.0

    symbol: str = ""

    timeframe: str = ""

    # =====================================================
    # Convenience Properties
    # =====================================================

    @property
    def is_buy(self):

        return self.side == SignalSide.BUY


    @property
    def is_sell(self):

        return self.side == SignalSide.SELL


    @property
    def is_neutral(self):

        return self.side == SignalSide.NEUTRAL
    
    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "StrategySignal("

            f"strategy={self.strategy}, "

            f"side={self.side}, "

            f"confidence={self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__