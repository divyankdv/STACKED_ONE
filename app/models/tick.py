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