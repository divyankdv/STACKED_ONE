"""
============================================================

                STACKED QUANT AI V6

            TIMEFRAME MANAGER

------------------------------------------------------------

Stores completed candles for all timeframes.

Responsibilities
----------------
✓ Store completed candles
✓ Return latest candle
✓ Return history
✓ Return last N candles

============================================================
"""

from collections import deque

from app.config.settings import settings


class TimeframeManager:

    def __init__(self):

        self.storage = {}

        for timeframe in settings.timeframes:

            self.storage[timeframe] = deque(
                maxlen=settings.max_candles
            )

    # =====================================================
    # Add Candle
    # =====================================================

    def add(self, timeframe, candle):

        if timeframe not in self.storage:

            raise ValueError(
                f"Unsupported timeframe: {timeframe}"
            )

        self.storage[timeframe].append(candle)

    # =====================================================
    # Last Candle
    # =====================================================

    def last(self, timeframe):

        candles = self.storage.get(timeframe)

        if not candles:

            return None

        return candles[-1]

    # =====================================================
    # Previous Candle
    # =====================================================

    def previous(self, timeframe):

        candles = self.storage.get(timeframe)

        if candles is None:

            return None

        if len(candles) < 2:

            return None

        return candles[-2]

    # =====================================================
    # History
    # =====================================================

    def history(self, timeframe):

        candles = self.storage.get(timeframe)

        if candles is None:

            return []

        return list(candles)

    # =====================================================
    # Last N
    # =====================================================

    def last_n(self, timeframe, n):

        candles = self.storage.get(timeframe)

        if candles is None:

            return []

        return list(candles)[-n:]

    # =====================================================
    # Count
    # =====================================================

    def count(self, timeframe):

        candles = self.storage.get(timeframe)

        if candles is None:

            return 0

        return len(candles)

    # =====================================================
    # Enough History?
    # =====================================================

    def has(self, timeframe, required):

        return self.count(timeframe) >= required

    # =====================================================
    # Supported Timeframes
    # =====================================================

    def timeframes(self):

        return list(self.storage.keys())

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        for candles in self.storage.values():

            candles.clear()