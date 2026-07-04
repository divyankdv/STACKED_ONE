"""
============================================================

                    STACKED ONE

                POSITION REDUCTION

------------------------------------------------------------

Represents the outcome of reducing or closing
an existing position.

Returned by:

    Position.reduce()

Consumed by:

    PositionManager
    Journal
    Performance
    EventBus

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PositionReduction:
    """
    Result returned when reducing a position.
    """

    # =====================================================
    # Quantity
    # =====================================================

    #
    # Quantity that was closed.
    #

    closed_quantity: float

    #
    # Quantity remaining in the position.
    #

    remaining_quantity: float

    # =====================================================
    # PnL
    # =====================================================

    realized_pnl: float

    # =====================================================
    # Status
    # =====================================================

    position_closed: bool

    #
    # True when execution quantity was larger than the
    # current position and a new opposite-side position
    # should be opened.
    #

    position_flipped: bool

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def partial_close(self) -> bool:
        """
        Position was reduced but is still open.
        """
        return (
            not self.position_closed
            and self.closed_quantity > 0
        )

    @property
    def full_close(self) -> bool:
        """
        Position fully closed.
        """
        return (
            self.position_closed
            and not self.position_flipped
        )

    @property
    def flip(self) -> bool:
        """
        Position reversed direction.
        """
        return self.position_flipped

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        if self.position_flipped:
            state = "FLIPPED"

        elif self.position_closed:
            state = "CLOSED"

        else:
            state = "REDUCED"

        return (
            "PositionReduction("
            f"{state}, "
            f"closed={self.closed_quantity:.6f}, "
            f"remaining={self.remaining_quantity:.6f}, "
            f"pnl={self.realized_pnl:.2f}"
            ")"
        )

    __repr__ = __str__