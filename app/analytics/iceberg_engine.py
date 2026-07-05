"""
============================================================

                    STACKED ONE

                ICEBERG ENGINE

------------------------------------------------------------

Detects potential iceberg orders by monitoring repeated
trading activity at the same price level.

Version 1.0

============================================================
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from app.analytics.base_engine import AnalyticsEngine
from app.analytics.iceberg_snapshot import IcebergSnapshot
from app.config.settings import settings


class IcebergEngine(AnalyticsEngine):

    snapshot_name = "iceberg"

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(

        self,

        volume_threshold: float | None = None,

        trade_threshold: int | None = None,

    ):

        self.volume_threshold = (

            volume_threshold
            if volume_threshold is not None
            else settings.iceberg_volume_threshold

        )

        self.trade_threshold = (

            trade_threshold
            if trade_threshold is not None
            else settings.iceberg_trade_threshold

        )

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.price_levels: defaultdict[
            float,
            dict[str, float | int],
        ] = defaultdict(

            lambda: {

                "volume": 0.0,

                "trades": 0,

                "buy_volume": 0.0,

                "sell_volume": 0.0,

            }

        )

        self.active = False

        self.side = "none"

        self.price = 0.0

        self.absorbed_volume = 0.0

        self.trade_count = 0

        self.confidence = 0.0

    # =====================================================
    # Update Trade
    # =====================================================

    def update_trade(

        self,

        trade,

    ):

        price = float(trade.price)

        level = self.price_levels[price]

        level["volume"] += trade.size

        level["trades"] += 1

        if trade.is_buy:

            level["buy_volume"] += trade.size

        else:

            level["sell_volume"] += trade.size

        self._evaluate(price)

    # =====================================================
    # Evaluate
    # =====================================================

    def _evaluate(

        self,

        price: float,

    ):

        level = self.price_levels[price]

        self.active = False

        self.confidence = 0.0

        if (

            level["volume"] < self.volume_threshold

            or

            level["trades"] < self.trade_threshold

        ):

            return

        self.active = True

        self.price = price

        self.absorbed_volume = level["volume"]

        self.trade_count = int(level["trades"])

        if level["buy_volume"] > level["sell_volume"]:

            self.side = "sell"

        else:

            self.side = "buy"

        volume_ratio = min(

            level["volume"] / self.volume_threshold,

            1.0,

        )

        trade_ratio = min(

            level["trades"] / self.trade_threshold,

            1.0,

        )

        self.confidence = (

            volume_ratio + trade_ratio

        ) / 2

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return IcebergSnapshot(

            active=self.active,

            side=self.side,

            price=self.price,

            absorbed_volume=self.absorbed_volume,

            trade_count=self.trade_count,

            confidence=self.confidence,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "IcebergEngine("

            f"active={self.active}, "

            f"side={self.side}, "

            f"price={self.price}, "

            f"confidence={self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__