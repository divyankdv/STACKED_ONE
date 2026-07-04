"""
============================================================

                    STACKED ONE

                  MESSAGE TYPES

============================================================
"""

from enum import Enum


class MessageType(str, Enum):

    SUBSCRIPTIONS = "subscriptions"

    ALL_TRADES = "all_trades"

    ALL_TRADES_SNAPSHOT = "all_trades_snapshot"

    L2_ORDERBOOK = "l2_orderbook"

    TICKER = "v2/ticker"

    FUNDING_RATE = "funding_rate"