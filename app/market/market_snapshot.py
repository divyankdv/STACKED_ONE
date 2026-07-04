"""
============================================================

                    STACKED ONE

                 MARKET SNAPSHOT

------------------------------------------------------------

Immutable snapshot of the current market state.

Every engine receives MarketSnapshot instead of
individual primitive parameters.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class MarketSnapshot:

    #
    # Identity
    #

    symbol: str

    timeframe: str

    timestamp: datetime

    #
    # Prices
    #

    last_price: float

    bid: float

    ask: float

    #
    # Volume
    #

    volume: float

    #
    # Spread
    #

    @property
    def spread(self) -> float:

        return self.ask - self.bid

    @property
    def mid_price(self) -> float:

        return (

            self.bid +

            self.ask

        ) / 2

    # =====================================================

    @property
    def valid(self) -> bool:

        return (

            self.bid > 0

            and

            self.ask > 0

            and

            self.last_price > 0

        )

    # =====================================================

    def __str__(self):

        return (

            "MarketSnapshot("

            f"{self.symbol}, "

            f"{self.last_price:.2f}, "

            f"spread={self.spread:.2f}"

            ")"

        )

    __repr__ = __str__