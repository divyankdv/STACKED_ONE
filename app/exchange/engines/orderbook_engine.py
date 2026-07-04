"""
============================================================

                STACKED QUANT AI V6

                ORDER BOOK ENGINE

------------------------------------------------------------

Receives order book updates from the exchange.

Responsibilities
----------------
✓ Update best bid / ask
✓ Calculate spread
✓ Calculate bid/ask imbalance
✓ Determine market pressure

============================================================
"""

from dataclasses import dataclass

from app.logger.logger import logger
from app.exchange.market_data import market_data


@dataclass
class OrderBookSnapshot:

    best_bid: float = 0.0
    best_ask: float = 0.0

    bid_size: float = 0.0
    ask_size: float = 0.0

    spread: float = 0.0

    imbalance: float = 0.0

    pressure: str = "NEUTRAL"


class OrderBookEngine:

    def __init__(self):

        self.snapshot = OrderBookSnapshot()

    # =====================================================
    # Update Order Book
    # =====================================================

    def update(
        self,
        best_bid,
        best_ask,
        bid_size,
        ask_size,
    ):

        try:

            best_bid = float(best_bid)
            best_ask = float(best_ask)

            bid_size = float(bid_size)
            ask_size = float(ask_size)

            # --------------------------------------------
            # Store latest values
            # --------------------------------------------

            self.snapshot.best_bid = best_bid
            self.snapshot.best_ask = best_ask

            self.snapshot.bid_size = bid_size
            self.snapshot.ask_size = ask_size

            # --------------------------------------------
            # Spread
            # --------------------------------------------

            self.snapshot.spread = best_ask - best_bid

            # --------------------------------------------
            # Imbalance
            # --------------------------------------------

            total = bid_size + ask_size

            if total > 0:

                imbalance = (bid_size - ask_size) / total

            else:

                imbalance = 0.0

            self.snapshot.imbalance = imbalance

            # --------------------------------------------
            # Market Pressure
            # --------------------------------------------

            if imbalance > 0.30:

                self.snapshot.pressure = "BUY"

            elif imbalance < -0.30:

                self.snapshot.pressure = "SELL"

            else:

                self.snapshot.pressure = "NEUTRAL"

            # --------------------------------------------
            # Update MarketData
            # --------------------------------------------

            market_data.update_orderbook(

                best_bid,

                best_ask,

                bid_size,

                ask_size,

            )

        except Exception as e:

            logger.error(f"OrderBookEngine : {e}")

    # =====================================================
    # Latest Snapshot
    # =====================================================

    def latest(self):

        return self.snapshot

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.snapshot = OrderBookSnapshot()