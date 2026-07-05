"""
============================================================

                    STACKED ONE

                 BROKER INTERFACE

------------------------------------------------------------

Abstract broker interface.

Every exchange implementation must inherit this class.

============================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.execution.order import Order
from app.execution.order_request import OrderRequest
from app.execution.order_result import OrderResult


class Broker(ABC):

    """
    Base broker interface.
    """

    # =====================================================
    # Submit
    # =====================================================

    @abstractmethod
    def submit_order(

        self,

        request: OrderRequest,

    ) -> OrderResult:
        """
        Submit a new order.
        """
        raise NotImplementedError

    # =====================================================
    # Cancel
    # =====================================================

    @abstractmethod
    def cancel_order(

        self,

        order: Order,

    ) -> bool:
        """
        Cancel an order.
        """
        raise NotImplementedError

    # =====================================================
    # Balance
    # =====================================================

    @abstractmethod
    def balance(self):

        raise NotImplementedError

    # =====================================================
    # Positions
    # =====================================================

    @abstractmethod
    def positions(self):

        raise NotImplementedError

    # =====================================================
    # Open Orders
    # =====================================================

    @abstractmethod
    def open_orders(self):

        raise NotImplementedError

    # =====================================================
    # Name
    # =====================================================

    @property
    def name(self):

        return self.__class__.__name__

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return self.name

    __repr__ = __str__