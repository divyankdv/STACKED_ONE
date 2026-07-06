"""
============================================================

                STACKED QUANT AI V6

                    TICK MODEL

Represents a single market trade.

============================================================
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tick:

    timestamp: datetime

    price: float

    volume: float

    side: str

    @property
    def size(self) -> float:
        return self.volume

    @property
    def is_buy(self) -> bool:
        return self.side.lower() == "buy"

    @property
    def is_sell(self) -> bool:
        return self.side.lower() == "sell"