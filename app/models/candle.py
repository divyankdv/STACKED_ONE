"""
============================================================

                STACKED QUANT AI V6

                CANDLE MODEL

Institutional OHLCV Candle

============================================================
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:

    time: datetime

    open: float

    high: float

    low: float

    close: float

    volume: float

    buy_volume: float

    sell_volume: float

    delta: float

    trades: int

    @property
    def body(self):

        return abs(self.close - self.open)

    @property
    def range(self):

        return self.high - self.low

    @property
    def bullish(self):

        return self.close > self.open

    @property
    def bearish(self):

        return self.close < self.open