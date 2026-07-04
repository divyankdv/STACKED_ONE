"""
============================================================

                    STACKED ONE

            ORDER FLOW SNAPSHOT

------------------------------------------------------------

Immutable snapshot of the current order flow state.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderFlowSnapshot:

    buy_volume: float

    sell_volume: float

    delta: float

    cvd: float

    total_volume: float

    total_value: float

    vwap: float

    trade_count: int

    buy_trades: int

    sell_trades: int

    largest_trade: float

    buy_aggression: float

    sell_aggression: float