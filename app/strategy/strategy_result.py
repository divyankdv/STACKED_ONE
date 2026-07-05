"""
============================================================

                    STACKED ONE

                STRATEGY RESULT

------------------------------------------------------------

Represents the output of the Strategy Engine.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.strategy.signal_side import SignalSide
from app.strategy.strategy_signal import StrategySignal


@dataclass(slots=True)
class StrategyResult:
    """
    Result produced by StrategyEngine.
    """

    # =====================================================
    # All Signals
    # =====================================================

    signals: tuple[StrategySignal, ...] = field(

        default_factory=tuple,

    )

    # =====================================================
    # Cached Best Signal
    # =====================================================

    best_signal: StrategySignal | None = None

    # =====================================================
    # BUY Signals
    # =====================================================

    @property
    def buy_signals(self) -> tuple[StrategySignal, ...]:

        return tuple(

            signal

            for signal in self.signals

            if signal.side == SignalSide.BUY

        )

    # =====================================================
    # SELL Signals
    # =====================================================

    @property
    def sell_signals(self) -> tuple[StrategySignal, ...]:

        return tuple(

            signal

            for signal in self.signals

            if signal.side == SignalSide.SELL

        )

    # =====================================================
    # Neutral Signals
    # =====================================================

    @property
    def neutral_signals(self) -> tuple[StrategySignal, ...]:

        return tuple(

            signal

            for signal in self.signals

            if signal.side == SignalSide.NEUTRAL

        )

    # =====================================================
    # Counts
    # =====================================================

    @property
    def buy_count(self) -> int:

        return len(

            self.buy_signals,

        )

    @property
    def sell_count(self) -> int:

        return len(

            self.sell_signals,

        )

    @property
    def neutral_count(self) -> int:

        return len(

            self.neutral_signals,

        )

    @property
    def strategy_count(self) -> int:

        return len(

            self.signals,

        )

    # =====================================================
    # Consensus
    # =====================================================

    @property
    def consensus(self) -> SignalSide:

        if self.buy_count > self.sell_count:

            return SignalSide.BUY

        if self.sell_count > self.buy_count:

            return SignalSide.SELL

        return SignalSide.NEUTRAL

    # =====================================================
    # Confidence
    # =====================================================

    @property
    def confidence(self) -> float:

        if self.best_signal is None:

            return 0.0

        return self.best_signal.confidence

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        best = (

            self.best_signal.strategy

            if self.best_signal

            else "None"

        )

        return (

            "StrategyResult("

            f"strategies={self.strategy_count}, "

            f"best={best}, "

            f"consensus={self.consensus.value}, "

            f"confidence={self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__