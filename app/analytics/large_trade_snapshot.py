"""
============================================================

                    STACKED ONE

             LARGE TRADE SNAPSHOT

------------------------------------------------------------

Immutable snapshot describing large trade activity.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LargeTradeSnapshot:

    total_large_trades: int

    buy_large_trades: int

    sell_large_trades: int

    largest_trade: float

    average_large_trade: float

    total_large_volume: float