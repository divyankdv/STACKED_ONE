"""
============================================================

                STACKED QUANT AI V6

                MARKET DATA

------------------------------------------------------------

Central storage for all real-time market information.

Every engine reads from here.

No engine should directly access the websocket.

============================================================
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketData:

    # ------------------------------------------------------
    # Instrument
    # ------------------------------------------------------

    symbol: str = "BTCUSD"

    # ------------------------------------------------------
    # Prices
    # ------------------------------------------------------

    mark_price: float = 0.0

    last_price: float = 0.0

    index_price: float = 0.0

    # ------------------------------------------------------
    # Order Book
    # ------------------------------------------------------

    best_bid: float = 0.0

    best_ask: float = 0.0

    bid_size: float = 0.0

    ask_size: float = 0.0

    # ------------------------------------------------------
    # Derivatives
    # ------------------------------------------------------

    funding_rate: float = 0.0

    open_interest: float = 0.0

    # ------------------------------------------------------
    # Timestamp
    # ------------------------------------------------------

    timestamp: datetime | None = None

    # ======================================================
    # Price Update
    # ======================================================

    def update_price(

        self,

        mark_price,

        last_price,

        index_price,

    ):

        self.mark_price = float(mark_price)

        self.last_price = float(last_price)

        self.index_price = float(index_price)

    # ======================================================
    # Orderbook Update
    # ======================================================

    def update_orderbook(

        self,

        best_bid,

        best_ask,

        bid_size,

        ask_size,

    ):

        self.best_bid = float(best_bid)

        self.best_ask = float(best_ask)

        self.bid_size = float(bid_size)

        self.ask_size = float(ask_size)

    # ======================================================
    # Funding
    # ======================================================

    def update_funding(

        self,

        funding,

    ):

        self.funding_rate = float(funding)

    # ======================================================
    # Open Interest
    # ======================================================

    def update_open_interest(

        self,

        oi,

    ):

        self.open_interest = float(oi)

    # ======================================================
    # Timestamp
    # ======================================================

    def update_timestamp(

        self,

        timestamp,

    ):

        self.timestamp = timestamp


market_data = MarketData()