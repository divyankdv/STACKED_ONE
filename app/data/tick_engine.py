"""
============================================================

                STACKED QUANT AI V6

                TICK ENGINE

------------------------------------------------------------

Receives every trade and builds 1-minute candles.

Responsibilities
----------------
✓ Build OHLC
✓ Build Volume
✓ Build Buy/Sell Volume
✓ Build Delta
✓ Count Trades
✓ Auto-close candle on minute change

============================================================
"""


from datetime import datetime

from app.models.candle import Candle
from app.models.tick import Tick


class TickEngine:

    def __init__(self):

        self.reset()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.current_minute: datetime | None = None

        self.open: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.close: float | None = None

        self.volume = 0.0

        self.buy_volume = 0.0
        self.sell_volume = 0.0

        self.delta = 0.0

        self.trades = 0

    # =====================================================
    # Start New Candle
    # =====================================================

    def _start_new_candle(self, tick: Tick):

        self.current_minute = tick.timestamp.replace(
            second=0,
            microsecond=0,
        )

        self.open = tick.price
        self.high = tick.price
        self.low = tick.price
        self.close = tick.price

        self.volume = tick.volume

        self.buy_volume = 0.0
        self.sell_volume = 0.0

        if tick.side.lower() == "buy":

            self.buy_volume = tick.volume
            self.delta = tick.volume

        else:

            self.sell_volume = tick.volume
            self.delta = -tick.volume

        self.trades = 1

    # =====================================================
    # Build Candle Object
    # =====================================================

    def build(self):

        if self.current_minute is None:

            return None
        
        if (
            self.open is None
            or self.high is None
            or self.low is None
            or self.close is None
        ):
            return None

        return Candle(

            time=self.current_minute,

            open=self.open,

            high=self.high,

            low=self.low,

            close=self.close,

            volume=self.volume,

            buy_volume=self.buy_volume,

            sell_volume=self.sell_volume,

            delta=self.delta,

            trades=self.trades,

        )

    # =====================================================
    # Update
    # =====================================================

    def update(self, tick: Tick):

        minute = tick.timestamp.replace(
            second=0,
            microsecond=0,
        )

        # ----------------------------------------------
        # First Tick
        # ----------------------------------------------

        if self.current_minute is None:

            self._start_new_candle(tick)

            return None

        # ----------------------------------------------
        # Minute Changed
        # ----------------------------------------------

        if minute != self.current_minute:

            completed = self.build()

            self.reset()

            self._start_new_candle(tick)

            return completed

        # ----------------------------------------------
        # Same Minute
        # ----------------------------------------------

        assert self.high is not None
        assert self.low is not None
        
        self.close = tick.price

        self.high = max(
            self.high,
            tick.price,
        )

        self.low = min(
            self.low,
            tick.price,
        )

        self.volume += tick.volume

        self.trades += 1

        if tick.side.lower() == "buy":

            self.buy_volume += tick.volume

            self.delta += tick.volume

        else:

            self.sell_volume += tick.volume

            self.delta -= tick.volume

        return None

    # =====================================================
    # Force Close
    # =====================================================

    def close_candle(self):

        candle = self.build()

        self.reset()

        return candle

    # =====================================================
    # Current State
    # =====================================================

    def current(self):

        return {

            "minute": self.current_minute,

            "open": self.open,

            "high": self.high,

            "low": self.low,

            "close": self.close,

            "volume": self.volume,

            "buy_volume": self.buy_volume,

            "sell_volume": self.sell_volume,

            "delta": self.delta,

            "trades": self.trades,

        }