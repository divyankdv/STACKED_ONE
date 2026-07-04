"""
============================================================

                    STACKED ONE

                  TRADE PARSER

------------------------------------------------------------

Parses Delta trade WebSocket messages into
TradeMessage objects.

Supports

✓ all_trades
✓ all_trades_snapshot

============================================================
"""

from __future__ import annotations

from app.exchange.protocol.trade_message import TradeMessage


class TradeParser:

    # =====================================================
    # Parse
    # =====================================================

    @staticmethod
    def parse(message: dict) -> list[TradeMessage]:

        message_type = message.get("type")

        #
        # Snapshot
        #

        if message_type == "all_trades_snapshot":

            symbol = message["symbol"]

            product_id = message.get("product_id", 0)

            trades = []

            for trade in message["trades"]:

                trade["symbol"] = symbol

                trade["product_id"] = product_id

                trade["buyer_role"] = trade["buyer_role"]

                trade["seller_role"] = trade["seller_role"]

                trades.append(

                    TradeMessage.from_delta(

                        trade

                    )

                )

            return trades

        #
        # Live Trade
        #

        if message_type == "all_trades":

            return [

                TradeMessage.from_delta(

                    message

                )

            ]

        return []