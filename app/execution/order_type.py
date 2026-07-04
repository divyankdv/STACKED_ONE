"""
============================================================

                    STACKED ONE

                  ORDER TYPE

============================================================
"""

from __future__ import annotations

from enum import Enum


class OrderType(str, Enum):

    MARKET = "MARKET"

    LIMIT = "LIMIT"

    STOP = "STOP"

    STOP_LIMIT = "STOP_LIMIT"