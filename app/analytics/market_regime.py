"""
============================================================

                    STACKED ONE

                 MARKET REGIME

============================================================
"""

from enum import StrEnum


class MarketRegime(StrEnum):

    UNKNOWN = "UNKNOWN"

    TREND_UP = "TREND_UP"

    TREND_DOWN = "TREND_DOWN"

    RANGE = "RANGE"

    ACCUMULATION = "ACCUMULATION"

    DISTRIBUTION = "DISTRIBUTION"

    BREAKOUT = "BREAKOUT"

    BREAKDOWN = "BREAKDOWN"