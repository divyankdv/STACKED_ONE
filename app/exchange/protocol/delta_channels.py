"""
============================================================

                    STACKED ONE

                DELTA CHANNELS

============================================================
"""

from enum import StrEnum


class DeltaChannel(StrEnum):

    TRADES = "all_trades"

    ORDERBOOK = "l2_orderbook"

    MARK_PRICE = "mark_price"

    FUNDING = "funding_rate"

    CANDLES = "candlestick"

    TICKER = "v2/ticker"