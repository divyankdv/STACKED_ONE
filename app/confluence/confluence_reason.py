"""
============================================================

                    STACKED ONE

              CONFLUENCE REASON

------------------------------------------------------------

Represents one reason contributing to the overall
trade confluence.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ConfluenceReason:
    """
    One piece of evidence supporting a trade.
    """

    #
    # Source
    #

    source: str

    #
    # Description
    #

    description: str

    #
    # Direction
    #

    bullish: bool

    #
    # Weight
    #

    weight: float = 1.0

    # =====================================================

    @property
    def bearish(self) -> bool:

        return not self.bullish

    # =====================================================

    def __str__(self):

        direction = "BUY" if self.bullish else "SELL"

        return (

            "ConfluenceReason("

            f"{direction}, "

            f"{self.source}, "

            f"weight={self.weight:.2f}"

            ")"

        )

    __repr__ = __str__