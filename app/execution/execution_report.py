"""
============================================================

                    STACKED ONE

                EXECUTION REPORT

------------------------------------------------------------

Immutable record of what the broker actually executed.

Produced by:
    Broker
        ↓
    ExecutionEngine

Consumed by:
    PositionManager
    Journal
    Performance
    Dashboard

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.execution.order_side import OrderSide
from app.execution.order_status import OrderStatus


@dataclass(slots=True, frozen=True)
class ExecutionReport:
    """
    Broker execution result.

    Represents a single execution/fill.
    """

    # =====================================================
    # Identity
    # =====================================================

    order_id: str

    exchange_order_id: str

    execution_id: str

    # =====================================================
    # Instrument
    # =====================================================

    symbol: str

    side: OrderSide

    # =====================================================
    # Requested
    # =====================================================

    requested_quantity: float

    requested_price: float

    # =====================================================
    # Executed
    # =====================================================

    executed_quantity: float

    executed_price: float

    status: OrderStatus

    # =====================================================
    # Costs
    # =====================================================

    commission: float = 0.0

    fees: float = 0.0

    # =====================================================
    # Timing
    # =====================================================

    executed_at: datetime = field(default_factory=datetime.utcnow)

    # =====================================================
    # Trade Management
    # =====================================================

    stop_price: float = 0.0

    target_price: float = 0.0

    # =====================================================
    # Metadata
    # =====================================================

    broker: str = ""

    message: str = ""

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def filled(self) -> bool:
        return self.status == OrderStatus.FILLED

    @property
    def partially_filled(self) -> bool:
        return self.status == OrderStatus.PARTIALLY_FILLED

    @property
    def rejected(self) -> bool:
        return self.status == OrderStatus.REJECTED

    @property
    def cancelled(self) -> bool:
        return self.status == OrderStatus.CANCELLED

    @property
    def notional(self) -> float:
        """
        Executed trade value.
        """
        return self.executed_quantity * self.executed_price

    @property
    def requested_notional(self) -> float:
        """
        Requested order value.
        """
        return self.requested_quantity * self.requested_price

    @property
    def slippage(self) -> float:
        """
        Positive means execution was worse than requested.
        """

        if self.side == OrderSide.BUY:
            return self.executed_price - self.requested_price

        return self.requested_price - self.executed_price

    @property
    def slippage_percent(self) -> float:

        if self.requested_price == 0:
            return 0.0

        return (self.slippage / self.requested_price) * 100.0

    @property
    def total_cost(self) -> float:
        """
        Commission + fees.
        """
        return self.commission + self.fees

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (
            "ExecutionReport("
            f"{self.symbol}, "
            f"{self.side.value}, "
            f"{self.executed_quantity:.6f} @ "
            f"{self.executed_price:.2f}, "
            f"{self.status.value}"
            ")"
        )

    __repr__ = __str__
