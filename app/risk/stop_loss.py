"""
============================================================

                    STACKED ONE

                  STOP LOSS ENGINE

------------------------------------------------------------

Calculates stop loss levels.

Current Version

    • Fixed %
    • ATR (future)
    • Structure (future)
    • Smart Money (future)

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.strategy.signal_side import SignalSide


@dataclass(slots=True)
class StopLoss:

    """
    Stop loss calculator.
    """

    #
    # Default Risk
    #

    default_percent: float = 0.005      # 0.50%

    minimum_distance: float = 0.10

    # =====================================================
    # Calculate
    # =====================================================

    def calculate(

        self,

        side: SignalSide,

        entry_price: float,

    ) -> float:

        if side == SignalSide.BUY:

            stop = (

                entry_price

                *

                (

                    1.0

                    -

                    self.default_percent

                )

            )

        elif side == SignalSide.SELL:

            stop = (

                entry_price

                *

                (

                    1.0

                    +

                    self.default_percent

                )

            )

        else:

            stop = entry_price

        #
        # Enforce minimum distance
        #

        distance = abs(

            entry_price -

            stop

        )

        if distance < self.minimum_distance:

            if side == SignalSide.BUY:

                stop = (

                    entry_price

                    -

                    self.minimum_distance

                )

            elif side == SignalSide.SELL:

                stop = (

                    entry_price

                    +

                    self.minimum_distance

                )

        return stop

    # =====================================================
    # Distance
    # =====================================================

    def distance(

        self,

        entry: float,

        stop: float,

    ) -> float:

        return abs(

            entry -

            stop

        )

    # =====================================================
    # Risk %
    # =====================================================

    def risk_percent(

        self,

        entry: float,

        stop: float,

    ) -> float:

        if entry == 0:

            return 0.0

        return (

            abs(

                entry -

                stop

            )

            /

            entry

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "StopLoss("

            f"default={self.default_percent:.2%}"

            ")"

        )

    __repr__ = __str__