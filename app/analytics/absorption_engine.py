"""
============================================================

                    STACKED ONE

                ABSORPTION ENGINE

------------------------------------------------------------

Detects simple bullish and bearish absorption.

Version 1.0

============================================================
"""

from __future__ import annotations

from collections import deque

from app.analytics.absorption_snapshot import AbsorptionSnapshot

from app.config.settings import settings

from app.analytics.base_engine import AnalyticsEngine


class AbsorptionEngine(AnalyticsEngine):

    snapshot_name = "absorption"

    """
    Detects absorption using a rolling trade window.

    Version 1 keeps the algorithm intentionally simple.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(

        self,

        window_size: int | None = None,

        volume_threshold: float | None = None,

        price_tolerance: float | None = None,

    ):

        self.window_size = (

            window_size

            if window_size is not None

            else settings.absorption_window_size

        )

        self.volume_threshold = (

            volume_threshold

            if volume_threshold is not None

            else settings.absorption_volume_threshold

        )

        self.price_tolerance = (

            price_tolerance

            if price_tolerance is not None

            else settings.absorption_price_tolerance

        )

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.trades = deque(maxlen=self.window_size)

        self.buy_volume = 0.0

        self.sell_volume = 0.0

        self.first_price = None

        self.last_price = None

        self.bullish_score = 0.0

        self.bearish_score = 0.0

        self.absorbed_volume = 0.0

        self.active = False

    # =====================================================
    # Update Trade
    # =====================================================

    def update_trade(self, trade):

        self.trades.append(trade)

        self.last_price = float(trade.price)

        if self.first_price is None:

            self.first_price = self.last_price

        self._recalculate()

    # =====================================================
    # Recalculate Window
    # =====================================================

    def _recalculate(self):

        self.buy_volume = 0.0
        self.sell_volume = 0.0

        if len(self.trades) < 2:

            return

        first = self.trades[0]
        last = self.trades[-1]

        self.first_price = float(first.price)
        self.last_price = float(last.price)

        for trade in self.trades:

            if trade.is_buy:

                self.buy_volume += trade.size

            elif trade.is_sell:

                self.sell_volume += trade.size

        price_change = self.last_price - self.first_price

        self.active = False

        self.bullish_score = 0.0
        self.bearish_score = 0.0
        self.absorbed_volume = 0.0

        # ------------------------------------------
        # Bullish Absorption
        # ------------------------------------------

        if (

            self.sell_volume >= self.volume_threshold

            and price_change > -self.price_tolerance

        ):

            self.active = True

            self.absorbed_volume = self.sell_volume

            self.bullish_score = min(

                self.sell_volume / self.volume_threshold,

                1.0,

            )

        # ------------------------------------------
        # Bearish Absorption
        # ------------------------------------------

        elif (

            self.buy_volume >= self.volume_threshold

            and price_change < self.price_tolerance

        ):

            self.active = True

            self.absorbed_volume = self.buy_volume

            self.bearish_score = min(

                self.buy_volume / self.volume_threshold,

                1.0,

            )

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return AbsorptionSnapshot(

            bullish_score=self.bullish_score,

            bearish_score=self.bearish_score,

            active=self.active,

            absorbed_volume=self.absorbed_volume,

            duration_seconds=0.0,

            last_price=self.last_price or 0.0,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "AbsorptionEngine("

            f"active={self.active}, "

            f"bullish={self.bullish_score:.2f}, "

            f"bearish={self.bearish_score:.2f}"

            ")"

        )

    __repr__ = __str__