"""
============================================================

                    STACKED ONE

                  RISK PROFILE

------------------------------------------------------------

Defines portfolio-wide risk constraints.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RiskProfile:
    """
    Trading risk configuration.
    """

    # =====================================================
    # Capital
    # =====================================================

    account_balance: float = 100000.0

    available_balance: float = 100000.0

    # =====================================================
    # Risk Limits
    # =====================================================

    risk_per_trade: float = 0.01

    max_daily_loss: float = 0.05

    max_open_positions: int = 3

    max_portfolio_risk: float = 0.03

    # =====================================================
    # Position Limits
    # =====================================================

    min_position_size: float = 1.0

    max_position_size: float = 100.0

    leverage: float = 1.0

    # =====================================================
    # Session State
    # =====================================================

    open_positions: int = 0

    daily_loss: float = 0.0

    # =====================================================
    # Properties
    # =====================================================

    @property
    def risk_amount(self) -> float:
        """
        Maximum amount willing to lose on one trade.
        """
        return self.account_balance * self.risk_per_trade

    @property
    def daily_loss_limit(self) -> float:
        """
        Maximum daily loss in account currency.
        """
        return self.account_balance * self.max_daily_loss

    @property
    def trading_allowed(self) -> bool:

        if self.daily_loss >= self.daily_loss_limit:
            return False

        if self.open_positions >= self.max_open_positions:
            return False

        return True

    # =====================================================
    # Session
    # =====================================================

    def register_position(self):

        self.open_positions += 1

    def close_position(self):

        if self.open_positions > 0:
            self.open_positions -= 1

    def register_loss(

        self,

        amount: float,

    ):

        self.daily_loss += abs(amount)

    def reset_session(self):

        self.open_positions = 0

        self.daily_loss = 0.0

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "RiskProfile("

            f"risk={self.risk_per_trade:.2%}, "

            f"open={self.open_positions}, "

            f"daily_loss={self.daily_loss:.2f}"

            ")"

        )

    __repr__ = __str__