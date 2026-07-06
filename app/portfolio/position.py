"""
============================================================

                    STACKED ONE

                     POSITION

------------------------------------------------------------

Represents a live trading position.

A Position is created from one or more ExecutionReports
and maintains the current portfolio state.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.execution.execution_report import ExecutionReport
from app.execution.order_side import OrderSide
from app.portfolio.position_reduction import PositionReduction


@dataclass(slots=True)
class Position:
    """
    Live trading position.
    """

    # =====================================================
    # Identity
    # =====================================================

    symbol: str

    side: OrderSide

    # =====================================================
    # State
    # =====================================================

    quantity: float = 0.0

    average_price: float = 0.0

    realized_pnl: float = 0.0

    unrealized_pnl: float = 0.0

    commission: float = 0.0

    fees: float = 0.0

    #
    # Trade Management
    #

    stop_price: float = 0.0

    target_price: float = 0.0

    # =====================================================
    # Lifecycle
    # =====================================================

    opened_at: datetime | None = None

    updated_at: datetime | None = None

    closed_at: datetime | None = None

    # =====================================================
    # Statistics
    # =====================================================

    execution_count: int = 0

    max_quantity: float = 0.0

    mfe: float = 0.0

    mae: float = 0.0

    # =====================================================
    # History
    # =====================================================

    executions: list[ExecutionReport] = field(
        default_factory=list
    )

    # =====================================================
    # Add Execution
    # =====================================================

    def add_execution(
        self,
        report: ExecutionReport,
    ) -> None:

        if report.symbol != self.symbol:
            raise ValueError(
                "Execution symbol mismatch."
            )

        #
        # Opening
        #

        if self.execution_count == 0:

            self.opened_at = report.executed_at

            self.average_price = report.executed_price

            self.quantity = report.executed_quantity

        else:

            #
            # Weighted Average Price
            #

            total_cost = (

                self.average_price * self.quantity

                +

                report.executed_price

                * report.executed_quantity

            )

            self.quantity += report.executed_quantity

            if self.quantity > 0:

                self.average_price = (

                    total_cost /

                    self.quantity

                )

        self.execution_count += 1

        self.updated_at = report.executed_at

        self.commission += report.commission

        self.fees += report.fees

        self.executions.append(report)

        self.max_quantity = max(

            self.max_quantity,

            self.quantity,

        )

        

    # =====================================================
    # Reduce Position
    # =====================================================

    def reduce(
        self,
        report: ExecutionReport,
    ) -> PositionReduction:

        """
        Reduce or close the position using an execution report.

        Returns
        -------
        float
            Realized PnL.
        """

        if report.symbol != self.symbol:
            raise ValueError(
                "Execution symbol mismatch."
            )

        quantity = min(
            report.executed_quantity,
            self.quantity,
        )

        if quantity <= 0:
            
            return PositionReduction(

                closed_quantity=0.0,

                remaining_quantity=self.quantity,

                realized_pnl=0.0,

                position_closed=False,

                position_flipped=False,

            )


        #
        # Calculate PnL
        #

        if self.side == OrderSide.BUY:

            pnl = (
                report.executed_price
                - self.average_price
            ) * quantity

        else:

            pnl = (
                self.average_price
                - report.executed_price
            ) * quantity

        #
        # Update Position
        #

        self.quantity -= quantity

        self.realized_pnl += pnl

        self.commission += report.commission

        self.fees += report.fees

        self.execution_count += 1

        self.updated_at = report.executed_at

        self.executions.append(report)

        #
        # Position Closed
        #

        if self.quantity == 0:

            self.closed_at = report.executed_at

        #
        # Was this execution larger than the position?
        #

        remaining_execution = max(

            report.executed_quantity - quantity,

            0.0,

        )

        return PositionReduction(

            closed_quantity=quantity,

            remaining_quantity=remaining_execution,

            realized_pnl=pnl,

            position_closed=self.quantity == 0,

            position_flipped=remaining_execution > 0,

        )

    
    
    # =====================================================
    # Mark To Market
    # =====================================================

    def mark_to_market(
        self,
        market_price: float,
    ) -> float:

        if self.side == OrderSide.BUY:

            self.unrealized_pnl = (

                market_price -

                self.average_price

            ) * self.quantity

        else:

            self.unrealized_pnl = (

                self.average_price -

                market_price

            ) * self.quantity

        self.mfe = max(

            self.mfe,

            self.unrealized_pnl,

        )

        self.mae = min(

            self.mae,

            self.unrealized_pnl,

        )

        return self.unrealized_pnl

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def is_open(self) -> bool:

        return self.quantity > 0

    @property
    def is_closed(self) -> bool:

        return not self.is_open

    @property
    def total_cost(self) -> float:

        return self.commission + self.fees

    @property
    def net_pnl(self) -> float:

        return (

            self.realized_pnl

            +

            self.unrealized_pnl

            -

            self.total_cost

        )

    @property
    def holding_time(self):

        if self.opened_at is None:

            return None

        end = self.closed_at or datetime.utcnow()

        return end - self.opened_at

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self.quantity = 0.0

        self.average_price = 0.0

        self.realized_pnl = 0.0

        self.unrealized_pnl = 0.0

        self.commission = 0.0

        self.fees = 0.0

        self.execution_count = 0

        self.max_quantity = 0.0

        self.mfe = 0.0

        self.mae = 0.0

        self.executions.clear()

        self.opened_at = None

        self.updated_at = None

        self.closed_at = None

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "Position("

            f"{self.symbol}, "

            f"{self.side.value}, "

            f"qty={self.quantity:.6f}, "

            f"avg={self.average_price:.2f}, "

            f"net={self.net_pnl:.2f}"

            ")"

        )

    __repr__ = __str__