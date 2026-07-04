"""
============================================================

                    STACKED ONE

                  TRADE MESSAGE

------------------------------------------------------------

Protocol model representing a single trade received from
Delta Exchange WebSocket.

Responsibilities
----------------
✓ Parse Delta trade JSON
✓ Convert to Domain Tick
✓ Provide helper properties

Never contains business logic.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from app.models.tick import Tick
from app.exchange.protocol.order_role import OrderRole


@dataclass(slots=True)
class TradeMessage:

    # =====================================================
    # Exchange Fields
    # =====================================================

    symbol: str

    product_id: int

    price: float

    size: float

    buyer_role: OrderRole

    seller_role: OrderRole

    timestamp: datetime

    # =====================================================
    # Parse Delta WebSocket Message
    # =====================================================

    @classmethod
    def from_delta(cls, data: dict) -> "TradeMessage":

        return cls(

            symbol=data["symbol"],

            product_id=int(data["product_id"]),

            price=float(data["price"]),

            size=float(data["size"]),

            buyer_role=OrderRole(data["buyer_role"]),

            seller_role=OrderRole(data["seller_role"]),

            timestamp=datetime.fromtimestamp(

                data["timestamp"] / 1_000_000,

                tz=UTC,

            ),

        )

    # =====================================================
    # Properties
    # =====================================================

    @property
    def is_buy(self) -> bool:
        """
        Aggressive buyer lifted the offer.
        """

        return self.buyer_role.is_taker

    @property
    def is_sell(self) -> bool:
        """
        Aggressive seller hit the bid.
        """

        return self.seller_role.is_taker

    @property
    def aggressor_side(self) -> str:
        """
        buy  -> buyer was taker
        sell -> seller was taker
        """

        if self.is_buy:
            return "buy"

        return "sell"

    @property
    def notional(self) -> float:

        return self.price * self.size

    # =====================================================
    # Convert To Domain Tick
    # =====================================================

    def to_tick(self) -> Tick:

        return Tick(

            timestamp=self.timestamp,

            price=self.price,

            volume=self.size,

            side=self.aggressor_side,

        )

    # =====================================================
    # Dictionary
    # =====================================================

    def to_dict(self) -> dict:

        return {

            "symbol": self.symbol,

            "product_id": self.product_id,

            "price": self.price,

            "size": self.size,

            "buyer_role": self.buyer_role.value,

            "seller_role": self.seller_role.value,

            "timestamp": self.timestamp,

            "aggressor_side": self.aggressor_side,

            "notional": self.notional,

        }

    # =====================================================
    # String Representation
    # =====================================================

    def __str__(self) -> str:

        return (

            f"TradeMessage("

            f"symbol={self.symbol}, "

            f"price={self.price}, "

            f"size={self.size}, "

            f"side={self.aggressor_side}, "

            f"time={self.timestamp.isoformat()}"

            f")"

        )

    __repr__ = __str__