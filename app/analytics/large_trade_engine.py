"""
============================================================

                    STACKED ONE

              LARGE TRADE ENGINE

------------------------------------------------------------

Tracks unusually large trades.

============================================================
"""

from __future__ import annotations

from app.analytics.base_engine import AnalyticsEngine
from app.analytics.large_trade_snapshot import LargeTradeSnapshot
from app.config.settings import settings


class LargeTradeEngine(AnalyticsEngine):

    snapshot_name = "large_trades"

    """
    Detects trades larger than a configurable threshold.
    """

    def __init__(

        self,

        threshold: float | None = None,

    ):

        self.threshold = (

            threshold

            if threshold is not None

            else settings.large_trade_threshold

        )

        self.reset()

    # =====================================================

    def reset(self):

        self.total_large_trades = 0

        self.buy_large_trades = 0

        self.sell_large_trades = 0

        self.total_large_volume = 0.0

        self.largest_trade = 0.0

    # =====================================================

    def update_trade(

        self,

        trade,

    ):

        size = float(trade.size)

        if size < self.threshold:

            return

        self.total_large_trades += 1

        self.total_large_volume += size

        if size > self.largest_trade:

            self.largest_trade = size

        if trade.is_buy:

            self.buy_large_trades += 1

        else:

            self.sell_large_trades += 1

    # =====================================================

    def snapshot(self):

        if self.total_large_trades == 0:

            average = 0.0

        else:

            average = (

                self.total_large_volume

                / self.total_large_trades

            )

        return LargeTradeSnapshot(

            total_large_trades=self.total_large_trades,

            buy_large_trades=self.buy_large_trades,

            sell_large_trades=self.sell_large_trades,

            largest_trade=self.largest_trade,

            average_large_trade=average,

            total_large_volume=self.total_large_volume,

        )

    # =====================================================

    def __str__(self):

        return (

            "LargeTradeEngine("

            f"count={self.total_large_trades}, "

            f"largest={self.largest_trade}"

            ")"

        )

    __repr__ = __str__