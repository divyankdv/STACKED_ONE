"""
============================================================

                    STACKED ONE

                FEATURE SNAPSHOT

------------------------------------------------------------

Unified feature vector used by AI and strategy engines.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureSnapshot:

    # -----------------------------
    # Order Flow
    # -----------------------------

    delta: float

    cvd: float

    buy_volume: float

    sell_volume: float

    buy_aggression: float

    sell_aggression: float

    largest_trade: float

    vwap: float

    # -----------------------------
    # Price
    # -----------------------------

    last_price: float

    # -----------------------------
    # Volume
    # -----------------------------

    total_volume: float

    trade_count: int