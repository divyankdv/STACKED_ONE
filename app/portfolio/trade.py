"""
============================================================

                STACKED ONE

                  TRADE MODEL

Represents one executed market trade.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Trade:

    timestamp: datetime

    price: float

    size: float

    is_buy: bool

    @property
    def is_sell(self) -> bool:
        return not self.is_buy