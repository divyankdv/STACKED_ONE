"""
============================================================

                    STACKED ONE

                 TRADE SIGNAL

------------------------------------------------------------

Represents one strategy output.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.decision.signal import Signal


@dataclass(slots=True, frozen=True)
class TradeSignal:
    #
    # Strategy
    #

    strategy: str

    #
    # Direction
    #

    signal: Signal

    #
    # Confidence
    #

    confidence: float

    #
    # Optional metadata
    #

    reason: str = ""

    timeframe: str = ""

    symbol: str = ""

    # =====================================================

    @property
    def actionable(self) -> bool:

        return self.signal is not Signal.FLAT
