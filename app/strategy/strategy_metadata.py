"""
============================================================

                    STACKED ONE

               STRATEGY METADATA

------------------------------------------------------------

Immutable metadata describing a strategy.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class StrategyMetadata:
    """
    Immutable strategy metadata.
    """

    #
    # Identity
    #

    name: str

    description: str

    version: str = "1.0"

    #
    # Configuration
    #

    enabled: bool = True

    #
    # Optional Classification
    #

    category: str = "General"

    timeframe: str = "Any"

    author: str = "STACKED ONE"

    # =====================================================

    def __str__(self):

        return (
            "StrategyMetadata("
            f"name={self.name}, "
            f"version={self.version}, "
            f"category={self.category}"
            ")"
        )

    __repr__ = __str__
