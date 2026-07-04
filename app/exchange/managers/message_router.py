"""
============================================================

                    STACKED ONE

                  MESSAGE ROUTER

------------------------------------------------------------

Routes incoming WebSocket messages to the
appropriate protocol parser.

Responsibilities
----------------
✓ Route messages
✓ Select parser

Never parses message contents.

============================================================
"""

from __future__ import annotations

from app.exchange.protocol.trade_parser import TradeParser
from app.exchange.protocol.message_type import MessageType


class MessageRouter:

    # =====================================================
    # Route
    # =====================================================

    def route(self, message: dict):

        message_type = message.get("type")

        #
        # Trade Messages
        #

        if message_type in (

            MessageType.ALL_TRADES.value,

            MessageType.ALL_TRADES_SNAPSHOT.value,

        ):

            return TradeParser.parse(message)

        #
        # Unknown
        #

        return []