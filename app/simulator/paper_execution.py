"""
============================================================

                    STACKED ONE

                PAPER EXECUTION

------------------------------------------------------------

Creates simulated ExecutionReports for exits during
historical replay.

Unlike ExecutionEngine, this class does not talk to
any broker.

============================================================
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.execution.execution_report import ExecutionReport
from app.execution.order_side import OrderSide
from app.execution.order_status import OrderStatus


class PaperExecution:
    """
    Generates synthetic execution reports during simulation.
    """

    # =====================================================
    # Close Position
    # =====================================================

    def close_position(
        self,
        position,
        exit_price: float,
    ) -> ExecutionReport:

        #
        # Reverse side
        #

        if position.side == OrderSide.BUY:
            side = OrderSide.SELL
        else:
            side = OrderSide.BUY

        return ExecutionReport(
            #
            # Identity
            #
            order_id=str(uuid4()),
            exchange_order_id="SIM_EXIT",
            execution_id=str(uuid4()),
            #
            # Instrument
            #
            symbol=position.symbol,
            side=side,
            #
            # Requested
            #
            requested_quantity=position.quantity,
            requested_price=exit_price,
            #
            # Executed
            #
            executed_quantity=position.quantity,
            executed_price=exit_price,
            status=OrderStatus.FILLED,
            #
            # Costs
            #
            commission=0.0,
            fees=0.0,
            #
            # Timing
            #
            executed_at=datetime.now(UTC),
            #
            # Metadata
            #
            broker="SIMULATOR",
            message="Historical Exit",
        )

    # =====================================================

    def __str__(self):

        return "PaperExecution()"

    __repr__ = __str__
