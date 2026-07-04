"""
============================================================

                STACKED QUANT AI V6

                CANDLE BUILDER

------------------------------------------------------------

Builds ONE candle from incoming ticks.

Responsibilities
----------------
✓ Receive ticks
✓ Build current candle
✓ Return completed candle

Does NOT
---------
✗ Store candle history
✗ Calculate indicators
✗ Make decisions

============================================================
"""

from __future__ import annotations

from copy import deepcopy

from app.models.candle import Candle


class CandleBuilder:

    def __init__(self):

        self.current = None

        self.last = None

        self.previous = None

        self.history = []

    # =====================================================
    # Update From Tick
    # =====================================================

    def update_tick(self, tick):

        """
        Build candles from incoming ticks.

        Returns:

            None
                Candle still forming

            Candle
                Completed candle
        """

        tick_time = tick.timestamp.replace(

            second=0,

            microsecond=0,

        )

        # ---------------------------------------------
        # First Tick
        # ---------------------------------------------

        if self.current is None:

            self.current = Candle(

                time=tick_time,

                open=tick.price,

                high=tick.price,

                low=tick.price,

                close=tick.price,

                volume=tick.volume,

                buy_volume=0.0,

                sell_volume=0.0,

                delta=0.0,

                trades=1,

            )

            return None

        # ---------------------------------------------
        # Same Candle
        # ---------------------------------------------

        if self.current.time == tick_time:

            self.current.high = max(

                self.current.high,

                tick.price,

            )

            self.current.low = min(

                self.current.low,

                tick.price,

            )

            self.current.close = tick.price

            self.current.volume += tick.volume

            return None

        # ---------------------------------------------
        # Candle Closed
        # ---------------------------------------------

        completed = deepcopy(

            self.current

        )

        self.previous = self.last

        self.last = completed

        self.history.append(

            completed

        )

        self.current = Candle(

            time=tick_time,

            open=tick.price,

            high=tick.price,

            low=tick.price,

            close=tick.price,

            volume=tick.volume,

            buy_volume=0.0,

            sell_volume=0.0,

            delta=0.0,

            trades=1,

        )

        return completed

    # =====================================================
    # Add Completed Candle
    # =====================================================

    def add_completed_candle(self, candle):

        """
        Used by HistoryLoader.

        Stores already completed candles.
        """

        self.previous = self.last

        self.last = candle

        self.history.append(candle)

    # =====================================================
    # Last N
    # =====================================================

    def last_n(self, n):

        return self.history[-n:]

    # =====================================================
    # Count
    # =====================================================

    @property
    def count(self):

        return len(self.history)

    # =====================================================
    # Has Enough History
    # =====================================================

    def has(self, candles):

        return len(self.history) >= candles

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.current = None

        self.last = None

        self.previous = None

        self.history.clear()