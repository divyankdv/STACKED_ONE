"""
============================================================

                    STACKED ONE

                   EXIT ENGINE

------------------------------------------------------------

Evaluates whether an open position should be closed.

Responsibilities

✓ Stop Loss
✓ Take Profit

Future

✓ Trailing Stop
✓ Time Exit
✓ Break Even
✓ Scale Out

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ExitReason(StrEnum):
    NONE = "NONE"

    STOP = "STOP"

    TARGET = "TARGET"


@dataclass(slots=True)
class ExitDecision:
    closed: bool

    exit_price: float = 0.0

    reason: ExitReason = ExitReason.NONE


class ExitEngine:
    """
    Determines whether an open trade should exit.
    """

    def evaluate(
        self,
        position,
        candle,
    ) -> ExitDecision:

        #
        # BUY
        #

        if position.side.value == "BUY":
            #
            # Stop Loss
            #

            if candle.low <= position.stop_price:
                return ExitDecision(
                    closed=True,
                    exit_price=position.stop_price,
                    reason=ExitReason.STOP,
                )

            #
            # Target
            #

            if candle.high >= position.target_price:
                return ExitDecision(
                    closed=True,
                    exit_price=position.target_price,
                    reason=ExitReason.TARGET,
                )

        #
        # SELL
        #

        else:
            #
            # Stop
            #

            if candle.high >= position.stop_price:
                return ExitDecision(
                    closed=True,
                    exit_price=position.stop_price,
                    reason=ExitReason.STOP,
                )

            #
            # Target
            #

            if candle.low <= position.target_price:
                return ExitDecision(
                    closed=True,
                    exit_price=position.target_price,
                    reason=ExitReason.TARGET,
                )

        return ExitDecision(
            closed=False,
        )

    def __str__(self):

        return "ExitEngine()"

    __repr__ = __str__
