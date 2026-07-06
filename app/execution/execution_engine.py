"""
============================================================

                    STACKED ONE

                EXECUTION ENGINE

------------------------------------------------------------

Converts approved TradePlans into broker executions.

Returns immutable ExecutionReports.

============================================================
"""

from __future__ import annotations

from app.execution.execution_report import ExecutionReport
from app.execution.execution_report_factory import ExecutionReportFactory
from app.execution.order_result import OrderResult
from app.execution.order_request import OrderRequest
from app.execution.order_side import OrderSide
from app.execution.order_type import OrderType
from app.risk.trade_plan import TradePlan
from app.strategy.signal_side import SignalSide


class ExecutionEngine:

    def __init__(
        self,
        broker,
    ) -> None:

        self.broker = broker

    # =====================================================

    def execute(
        self,
        trade_plan: TradePlan,
    ) -> ExecutionReport | None:

        #
        # Reject
        #

        if not trade_plan.approved:
            return None

        #
        # Side
        #

        if trade_plan.side == SignalSide.BUY:

            side = OrderSide.BUY

        elif trade_plan.side == SignalSide.SELL:

            side = OrderSide.SELL

        else:

            return None

        #
        # Request
        #

        request = OrderRequest(

            symbol=trade_plan.symbol,

            side=side,

            order_type=OrderType.MARKET,

            quantity=trade_plan.position_size,

            price=trade_plan.entry_price,

            stop_price=trade_plan.stop_price,

            client_tag="STACKED_ONE",

        )

        #
        # Broker
        #

        result: OrderResult = self.broker.submit_order(

            request,

        )

        if not result.success:

            return None

        #
        # Build report
        #

        report = ExecutionReportFactory.create(

            result,

        )

        #
        # Inject trade management
        #

        object.__setattr__(

            report,

            "stop_price",

            trade_plan.stop_price,

        )

        object.__setattr__(

            report,

            "target_price",

            trade_plan.target_price,

        )

        return report

    # =====================================================

    def __str__(self):

        return "ExecutionEngine()"

    __repr__ = __str__