"""
============================================================

            STACKED QUANT AI V6

            CANDLE SERIES MODEL

A collection of candles belonging to one timeframe.

============================================================
"""

from dataclasses import dataclass, field

from app.models.candle import Candle


@dataclass
class CandleSeries:

    timeframe: int

    candles: list[Candle] = field(default_factory=list)

    def add(self, candle: Candle):

        self.candles.append(candle)

    def last(self):

        if not self.candles:

            return None

        return self.candles[-1]

    def last_n(self, n):

        return self.candles[-n:]

    def size(self):

        return len(self.candles)

    def clear(self):

        self.candles.clear()