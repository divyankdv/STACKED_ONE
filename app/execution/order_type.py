"""
============================================================

                    STACKED ONE

                  ORDER TYPE

============================================================
"""

from __future__ import annotations

from enum import StrEnum


class OrderType(StrEnum):

    MARKET = "MARKET"

    LIMIT = "LIMIT"

    STOP = "STOP"

    STOP_LIMIT = "STOP_LIMIT"