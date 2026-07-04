"""
============================================================

                    STACKED ONE

                ORDER FLOW ENGINE

------------------------------------------------------------

Maintains running order flow statistics.

Consumes TradeMessage objects.

Produces immutable OrderFlowSnapshot objects.

============================================================
"""

from __future__ import annotations

from app.analytics.order_flow_snapshot import OrderFlowSnapshot

from app.analytics.base_engine import AnalyticsEngine


class OrderFlowEngine(AnalyticsEngine):

    snapshot_name = "order_flow"

    """
    Real-time Order Flow Engine.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.buy_volume = 0.0
        self.sell_volume = 0.0

        self.buy_trades = 0
        self.sell_trades = 0

        self.trade_count = 0

        self.delta = 0.0
        self.cvd = 0.0

        self.total_volume = 0.0
        self.total_value = 0.0

        self.largest_trade = 0.0

    # =====================================================
    # Update Trade
    # =====================================================

    def update_trade(

        self,

        trade,

    ):

        size = float(trade.size)
        price = float(trade.price)

        self.trade_count += 1

        self.total_volume += size
        self.total_value += price * size

        if size > self.largest_trade:

            self.largest_trade = size

        if trade.is_buy:

            self.buy_volume += size
            self.buy_trades += 1

            self.delta += size
            self.cvd += size

        elif trade.is_sell:

            self.sell_volume += size
            self.sell_trades += 1

            self.delta -= size
            self.cvd -= size

    # =====================================================
    # VWAP
    # =====================================================

    @property
    def vwap(self):

        if self.total_volume == 0:

            return 0.0

        return self.total_value / self.total_volume

    # =====================================================
    # Buy Aggression
    # =====================================================

    @property
    def buy_aggression(self):

        if self.total_volume == 0:

            return 0.0

        return (self.buy_volume / self.total_volume) * 100

    # =====================================================
    # Sell Aggression
    # =====================================================

    @property
    def sell_aggression(self):

        return 100.0 - self.buy_aggression

    # =====================================================
    # Snapshot
    # =====================================================

    def snapshot(self):

        return OrderFlowSnapshot(

            buy_volume=self.buy_volume,

            sell_volume=self.sell_volume,

            delta=self.delta,

            cvd=self.cvd,

            total_volume=self.total_volume,

            total_value=self.total_value,

            vwap=self.vwap,

            trade_count=self.trade_count,

            buy_trades=self.buy_trades,

            sell_trades=self.sell_trades,

            largest_trade=self.largest_trade,

            buy_aggression=self.buy_aggression,

            sell_aggression=self.sell_aggression,

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            f"OrderFlowEngine("

            f"Trades={self.trade_count}, "

            f"Delta={self.delta:.2f}, "

            f"CVD={self.cvd:.2f})"

        )

    __repr__ = __str__