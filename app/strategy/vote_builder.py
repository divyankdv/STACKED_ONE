"""
============================================================

                    STACKED ONE

                  VOTE BUILDER

------------------------------------------------------------

Collects directional votes from strategy conditions.

Used together with ConfidenceBuilder and
DecisionPolicy.

============================================================
"""

from __future__ import annotations


class VoteBuilder:
    """
    Collects bullish and bearish votes.

    Every satisfied condition contributes one directional
    vote together with a human-readable explanation.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self._bullish = 0

        self._bearish = 0

        self._bullish_reasons: list[str] = []

        self._bearish_reasons: list[str] = []

    # =====================================================
    # Bullish Vote
    # =====================================================

    def bullish(
        self,
        condition: bool,
        reason: str,
    ) -> bool:

        if condition:
            self._bullish += 1

            self._bullish_reasons.append(reason)

        return condition

    # =====================================================
    # Bearish Vote
    # =====================================================

    def bearish(
        self,
        condition: bool,
        reason: str,
    ) -> bool:

        if condition:
            self._bearish += 1

            self._bearish_reasons.append(reason)

        return condition

    # =====================================================
    # Properties
    # =====================================================

    @property
    def bullish_votes(self) -> int:

        return self._bullish

    @property
    def bearish_votes(self) -> int:

        return self._bearish

    @property
    def total_votes(self) -> int:

        return self._bullish + self._bearish

    @property
    def bullish_reasons(self) -> tuple[str, ...]:

        return tuple(self._bullish_reasons)

    @property
    def bearish_reasons(self) -> tuple[str, ...]:

        return tuple(self._bearish_reasons)

    @property
    def all_reasons(self) -> tuple[str, ...]:

        return tuple(self._bullish_reasons + self._bearish_reasons)

    @property
    def dominant_side(self) -> str:

        if self._bullish > self._bearish:
            return "BUY"

        if self._bearish > self._bullish:
            return "SELL"

        return "NEUTRAL"

    @property
    def consensus(self) -> float:

        total = self.total_votes

        if total == 0:
            return 0.0

        return abs(self._bullish - self._bearish) / total

    @property
    def empty(self) -> bool:

        return self.total_votes == 0

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (
            "VoteBuilder("
            f"bullish={self._bullish}, "
            f"bearish={self._bearish}, "
            f"consensus={self.consensus:.2f}"
            ")"
        )

    __repr__ = __str__
