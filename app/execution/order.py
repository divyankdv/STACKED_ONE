"""
============================================================

                    STACKED ONE

                     ORDER

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

from app.execution.order_request import OrderRequest
from app.execution.order_status import OrderStatus


@dataclass(slots=True)
class Order:

    """
    Live order tracked by the OMS.
    """

    request: OrderRequest

    status: OrderStatus = OrderStatus.PENDING

    filled_quantity: float = 0.0

    average_fill_price: float = 0.0

    exchange_order_id: str = ""

    created_at: datetime = field(

        default_factory=datetime.utcnow

    )

    updated_at: datetime = field(

        default_factory=datetime.utcnow

    )

    @property
    def remaining_quantity(self):

        return (

            self.request.quantity -

            self.filled_quantity

        )

    @property
    def completed(self):

        return self.status == OrderStatus.FILLED

    def __str__(self):

        return (

            "Order("

            f"{self.request.symbol}, "

            f"{self.status.value}"

            ")"

        )

    __repr__ = __str__