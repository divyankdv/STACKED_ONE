"""
============================================================

                    STACKED ONE

                TAKE PROFIT ENGINE

------------------------------------------------------------

Calculates profit targets based on:

    • Entry Price
    • Stop Loss
    • Risk Reward Ratio

Future Versions

    • ATR Targets
    • Liquidity Targets
    • Smart Money Targets
    • Multi-Level Targets

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.strategy.signal_side import SignalSide


@dataclass(slots=True)
class TakeProfit:

    """
    Calculates take-profit levels.
    """

    #
    # Default Risk Reward
    #

    rr_ratio: float = 3.0

    # =====================================================
    # Calculate
    # =====================================================

    def calculate(

        self,

        side: SignalSide,

        entry_price: float,

        stop_price: float,

    ) -> float:

        """
        Calculates take-profit using
        Risk : Reward ratio.
        """

        risk = abs(

            entry_price -

            stop_price

        )

        reward = risk * self.rr_ratio

        if side == SignalSide.BUY:

            return (

                entry_price +

                reward

            )

        if side == SignalSide.SELL:

            return (

                entry_price -

                reward

            )

        return entry_price

    # =====================================================
    # Reward Distance
    # =====================================================

    def reward(

        self,

        entry_price: float,

        target_price: float,

    ) -> float:

        return abs(

            target_price -

            entry_price

        )

    # =====================================================
    # Reward %
    # =====================================================

    def reward_percent(

        self,

        entry_price: float,

        target_price: float,

    ) -> float:

        if entry_price == 0:

            return 0.0

        return (

            abs(

                target_price -

                entry_price

            )

            /

            entry_price

        )

    # =====================================================
    # Actual RR
    # =====================================================

    def risk_reward(

        self,

        entry_price: float,

        stop_price: float,

        target_price: float,

    ) -> float:

        risk = abs(

            entry_price -

            stop_price

        )

        if risk == 0:

            return 0.0

        reward = abs(

            target_price -

            entry_price

        )

        return reward / risk

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "TakeProfit("

            f"RR={self.rr_ratio:.1f}"

            ")"

        )

    __repr__ = __str__