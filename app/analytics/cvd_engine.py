"""
============================================================

                    STACKED ONE

                CVD ENGINE

------------------------------------------------------------

Maintains the running Cumulative Volume Delta.

Consumes TradeMessage objects.

Produces immutable CVDSnapshot objects.

============================================================
"""

from __future__ import annotations

from app.analytics.cvd_snapshot import CVDSnapshot

from app.analytics.base_engine import AnalyticsEngine


class CVDEngine(AnalyticsEngine):

    snapshot_name = "cvd"

    """
    Running Cumulative Volume Delta.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset Session
    # =====================================================

    def reset(self):

        self.current = 0.0

        self.highest = 0.0

        self.lowest = 0.0

        self.session_open = 0.0

        self.trade_count = 0

    # =====================================================
    # Update Trade
    # =====================================================

    def update_trade(self, trade):

        self.trade_count += 1

        volume = float(trade.size)

        if trade.is_buy:

            self.current += volume

        elif trade.is_sell:

            self.current -= volume

        if self.current > self.highest:

            self.highest = self.current

        if self.current < self.lowest:

            self.lowest = self.current

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return CVDSnapshot(

            current=self.current,

            highest=self.highest,

            lowest=self.lowest,

            session_open=self.session_open,

            trade_count=self.trade_count,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            f"CVDEngine("

            f"CVD={self.current:.2f}, "

            f"High={self.highest:.2f}, "

            f"Low={self.lowest:.2f}, "

            f"Trades={self.trade_count}"

            f")"

        )

    __repr__ = __str__