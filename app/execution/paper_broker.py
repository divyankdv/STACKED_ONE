"""
============================================================

                    STACKED ONE

                  PAPER BROKER

------------------------------------------------------------

Simulated execution.

No real orders are sent.

============================================================
"""

from __future__ import annotations

from datetime import datetime

from app.execution.broker import Broker
from app.execution.order import Order
from app.execution.order_request import OrderRequest
from app.execution.order_result import OrderResult
from app.execution.order_status import OrderStatus


class PaperBroker(Broker):
    """
    Paper trading broker.
    """

    # =====================================================

    def __init__(self):

        self.orders: list[Order] = []

    # =====================================================

    def submit_order(
        self,
        request: OrderRequest,
    ) -> OrderResult:

        order = Order(
            request=request,
            status=OrderStatus.FILLED,
            filled_quantity=request.quantity,
            average_fill_price=request.price,
            exchange_order_id=f"PAPER-{len(self.orders) + 1}",
            updated_at=datetime.utcnow(),
        )

        self.orders.append(
            order,
        )

        return OrderResult(
            success=True,
            message="Paper order filled.",
            order=order,
        )

    # =====================================================

    def cancel_order(
        self,
        order: Order,
    ) -> bool:

        if order.completed:
            return False

        order.status = OrderStatus.CANCELLED
        order.updated_at = datetime.utcnow()

        return True

    # =====================================================

    def balance(self):

        return {
            "currency": "USD",
            "balance": 100000.0,
            "available": 100000.0,
        }

    # =====================================================

    def positions(self):

        return []

    # =====================================================

    def open_orders(self):

        return [order for order in self.orders if order.status != OrderStatus.FILLED]

    # =====================================================

    def reset(self):

        self.orders.clear()

    # =====================================================

    def __len__(self):

        return len(self.orders)
