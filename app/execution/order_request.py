"""
============================================================

                    STACKED ONE

                 ORDER REQUEST

------------------------------------------------------------

Represents an order request created by the
Execution Engine.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from app.execution.order_side import OrderSide
from app.execution.order_type import OrderType


@dataclass(slots=True)
class OrderRequest:

    """
    Order submitted to a broker.
    """

    #
    # Identity
    #

    order_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    #
    # Instrument
    #

    symbol: str = ""

    #
    # Side
    #

    side: OrderSide = OrderSide.BUY

    #
    # Order Type
    #

    order_type: OrderType = OrderType.MARKET

    #
    # Quantity
    #

    quantity: float = 0.0

    #
    # Price
    #

    price: float = 0.0

    #
    # Optional Stop Price
    #

    stop_price: float = 0.0

    #
    # Reduce Only
    #

    reduce_only: bool = False

    #
    # Client Tag
    #

    client_tag: str = ""

    def __str__(self):

        return (

            "OrderRequest("

            f"{self.side.value}, "

            f"{self.quantity:.4f}, "

            f"{self.symbol}"

            ")"

        )

    __repr__ = __str__