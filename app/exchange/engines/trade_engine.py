"""
============================================================

                STACKED QUANT AI V6

                  TRADE ENGINE

------------------------------------------------------------

Receives raw trades from the exchange.

Converts them into Tick objects.

Responsibilities
----------------
✓ Parse exchange trade
✓ Validate trade
✓ Convert to Tick model

Does NOT
---------
✗ Build candles
✗ Calculate indicators
✗ Make decisions

============================================================
"""

from datetime import datetime

from app.logger.logger import logger
from app.models.tick import Tick


class TradeEngine:

    def __init__(self):

        self.last_trade = None

        self.trade_count = 0

    # =====================================================
    # Process Exchange Trade
    # =====================================================

    def process(self, trade):

        """
        Convert raw exchange trade into Tick object.
        """

        try:

            price = float(
                trade.get("price", 0)
            )

            volume = float(
                trade.get("size", 0)
            )

            # Delta Exchange uses buyer_role
            buyer_role = trade.get(
                "buyer_role",
                "taker",
            ).lower()

            # Infer trade direction
            if buyer_role == "maker":

                side = "sell"

            else:

                side = "buy"

            timestamp = trade.get(
                "timestamp"
            )

            if timestamp:

                timestamp = datetime.fromisoformat(
                    timestamp.replace(
                        "Z",
                        "+00:00",
                    )
                )

            else:

                timestamp = datetime.utcnow()

            tick = Tick(

                timestamp=timestamp,

                price=price,

                volume=volume,

                side=side,

            )

            self.last_trade = tick

            self.trade_count += 1

            return tick

        except Exception:

            logger.exception("TradeEngine processing failed")

            return None

    # =====================================================
    # Latest Tick
    # =====================================================

    def latest(self):

        return self.last_trade

    # =====================================================
    # Statistics
    # =====================================================

    def stats(self):

        return {

            "trades": self.trade_count,

            "last_price": (
                self.last_trade.price
                if self.last_trade
                else None
            ),

        }

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.last_trade = None

        self.trade_count = 0