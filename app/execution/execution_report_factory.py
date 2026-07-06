"""
============================================================

                    STACKED ONE

            EXECUTION REPORT FACTORY

------------------------------------------------------------

Converts broker OrderResults into immutable
ExecutionReports.

============================================================
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.execution.execution_report import ExecutionReport
from app.execution.order_result import OrderResult


class ExecutionReportFactory:
    """
    Creates ExecutionReports from broker OrderResults.
    """

    @staticmethod
    def create(
        result: OrderResult,
    ) -> ExecutionReport:

        if result.order is None:
            raise ValueError("OrderResult contains no Order.")

        order = result.order
        request = order.request

        return ExecutionReport(
            #
            # Identity
            #
            order_id=str(uuid4()),
            exchange_order_id=order.exchange_order_id,
            execution_id=str(uuid4()),
            #
            # Instrument
            #
            symbol=request.symbol,
            side=request.side,
            #
            # Requested
            #
            requested_quantity=request.quantity,
            requested_price=request.price,
            #
            # Executed
            #
            executed_quantity=order.filled_quantity,
            executed_price=order.average_fill_price,
            status=order.status,
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
            broker="PaperBroker",
            message=result.message,
        )
