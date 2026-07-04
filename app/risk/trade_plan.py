"""
============================================================

                    STACKED ONE

                   TRADE PLAN

------------------------------------------------------------

Represents a complete executable trading plan produced
by the Risk Engine.

The Execution Engine consumes this object directly.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from app.strategy.signal_side import SignalSide


@dataclass(slots=True)
class TradePlan:

    """
    Complete execution plan.
    """

    # =====================================================
    # Decision
    # =====================================================

    approved: bool

    reason: str

    side: SignalSide

    # =====================================================
    # Prices
    # =====================================================

    entry_price: float

    stop_price: float

    target_price: float

    # =====================================================
    # Position
    # =====================================================

    position_size: float

    exposure: float

    leverage: float

    # =====================================================
    # Risk
    # =====================================================

    risk_amount: float

    reward_amount: float

    risk_reward: float

    # =====================================================
    # Confidence
    # =====================================================

    confidence: float

    agreement: float

    # =====================================================
    # Metadata
    # =====================================================

    strategy: str = ""

    symbol: str = ""

    timeframe: str = ""

    notes: tuple[str, ...] = field(

        default_factory=tuple,

    )

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def rejected(self) -> bool:

        return not self.approved

    @property
    def expected_profit(self) -> float:

        return self.reward_amount

    @property
    def expected_loss(self) -> float:

        return self.risk_amount

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "TradePlan("

            f"approved={self.approved}, "

            f"side={self.side.value}, "

            f"entry={self.entry_price:.2f}, "

            f"stop={self.stop_price:.2f}, "

            f"target={self.target_price:.2f}, "

            f"size={self.position_size:.4f}, "

            f"RR={self.risk_reward:.2f}"

            ")"

        )

    __repr__ = __str__