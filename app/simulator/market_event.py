"""
============================================================

                    STACKED ONE

                  MARKET EVENT

------------------------------------------------------------

Represents a single market event.

Designed for replay, simulation, paper trading
and future backtesting.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class MarketEvent:
    """
    Immutable market event.
    """

    # =====================================================
    # Identity
    # =====================================================

    trade_id: str

    exchange: str

    symbol: str

    timestamp: datetime

    # =====================================================
    # Trade Data
    # =====================================================

    price: float

    quantity: float

    # =====================================================
    # Aggressor
    # =====================================================

    is_buyer_maker: bool | None = None

    #
    # False -> Buyer initiated
    # True  -> Seller initiated
    #

    # =====================================================
    # Order Book
    # =====================================================

    bid: float = 0.0

    ask: float = 0.0

    bid_size: float = 0.0

    ask_size: float = 0.0

    # =====================================================
    # Optional
    # =====================================================

    sequence: int = 0

    local_timestamp: datetime | None = None

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def volume(self) -> float:
        return self.quantity

    @property
    def spread(self) -> float:
        return self.ask - self.bid

    @property
    def mid_price(self) -> float:

        if self.bid == 0 or self.ask == 0:
            return self.price

        return (self.bid + self.ask) / 2

    @property
    def aggressive_buy(self) -> bool:

        if self.is_buyer_maker is None:
            return False

        return not self.is_buyer_maker

    @property
    def aggressive_sell(self) -> bool:

        if self.is_buyer_maker is None:
            return False

        return self.is_buyer_maker

    @property
    def has_orderbook(self) -> bool:

        return (

            self.bid > 0

            and

            self.ask > 0

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        side = "UNKNOWN"

        if self.aggressive_buy:
            side = "BUY"

        elif self.aggressive_sell:
            side = "SELL"

        return (

            "MarketEvent("

            f"{self.symbol}, "

            f"{side}, "

            f"{self.price:.2f}, "

            f"{self.quantity:.4f}"

            ")"

        )

    __repr__ = __str__