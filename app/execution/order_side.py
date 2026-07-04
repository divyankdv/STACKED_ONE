"""
============================================================

                    STACKED ONE

                  ORDER SIDE

============================================================
"""

from __future__ import annotations

from enum import Enum


class OrderSide(str, Enum):

    BUY = "BUY"

    SELL = "SELL"