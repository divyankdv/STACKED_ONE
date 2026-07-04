"""
============================================================

                    STACKED ONE

                 POSITION SIZE

------------------------------------------------------------

Calculates the appropriate position size based on:

    • Account Balance
    • Risk Per Trade
    • Entry Price
    • Stop Loss
    • Leverage

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.risk.risk_profile import RiskProfile


@dataclass(slots=True, frozen=True)
class PositionSize:

    """
    Position sizing calculator.
    """

    risk_profile: RiskProfile

    # =====================================================
    # Calculate
    # =====================================================

    def calculate(

        self,

        entry_price: float,

        stop_price: float,

    ) -> float:

        """
        Calculates the maximum position size.

        Formula

        Position Size =
            Risk Amount
            ---------------------
            Entry - Stop
        """

        risk_distance = abs(

            entry_price -

            stop_price

        )

        if risk_distance <= 0:

            return 0.0

        risk_amount = (

            self.risk_profile.risk_amount

        )

        position_size = (

            risk_amount /

            risk_distance

        )

        #
        # Apply leverage
        #

        position_size *= (

            self.risk_profile.leverage

        )

        #
        # Clamp
        #

        position_size = max(

            self.risk_profile.min_position_size,

            position_size,

        )

        position_size = min(

            self.risk_profile.max_position_size,

            position_size,

        )

        return position_size

    # =====================================================
    # Dollar Exposure
    # =====================================================

    def exposure(

        self,

        position_size: float,

        entry_price: float,

    ) -> float:

        return (

            position_size *

            entry_price

        )

    # =====================================================
    # Risk
    # =====================================================

    def monetary_risk(

        self,

        position_size: float,

        entry_price: float,

        stop_price: float,

    ) -> float:

        return (

            abs(

                entry_price -

                stop_price

            )

            *

            position_size

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "PositionSize("

            f"risk={self.risk_profile.risk_per_trade:.2%}"

            ")"

        )

    __repr__ = __str__