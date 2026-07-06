"""
============================================================

                    STACKED ONE

                EXECUTION ENGINE

------------------------------------------------------------

Converts TradePlans into executable broker orders.

Responsibilities

✓ Validate TradePlan
✓ Build OrderRequest
✓ Submit to Broker
✓ Return OrderResult

============================================================
"""

from __future__ import annotations

from app.execution.broker import Broker
from app.execution.order_request import OrderRequest
from app.execution.order_result import OrderResult
from app.execution.order_side import OrderSide
from app.execution.order_type import OrderType
from app.execution.paper_broker import PaperBroker
from app.market.market_snapshot import MarketSnapshot
from app.risk.trade_plan import TradePlan
from app.strategy.signal_side import SignalSide


class ExecutionEngine:
    """
    Executes approved TradePlans.
    """

    # =====================================================

    def __init__(
        self,
        broker: Broker | None = None,
    ):

        #
        # Default to paper trading.
        #

        self.broker = broker or PaperBroker()

    # =====================================================

    def execute(
        self,
        trade_plan: TradePlan,
        market: MarketSnapshot,
    ) -> OrderResult:

        #
        # Reject invalid plans
        #

        if not trade_plan.approved:
            return OrderResult(
                success=False,
                message="; ".join(trade_plan.notes),
                order=None,
            )

        #
        # Reject invalid market
        #

        if not market.valid:
            return OrderResult(
                success=False,
                message="Invalid market snapshot.",
                order=None,
            )

        #
        # Convert side
        #

        if trade_plan.side == SignalSide.BUY:
            side = OrderSide.BUY

        elif trade_plan.side == SignalSide.SELL:
            side = OrderSide.SELL

        else:
            return OrderResult(
                success=False,
                message="Neutral trade plan.",
                order=None,
            )

        #
        # Decide execution price
        #

        if side == OrderSide.BUY:
            execution_price = market.ask

        else:
            execution_price = market.bid

        #
        # Build OrderRequest
        #

        request = OrderRequest(
            symbol=trade_plan.symbol,
            side=side,
            order_type=OrderType.MARKET,
            quantity=trade_plan.position_size,
            price=execution_price,
            stop_price=trade_plan.stop_price,
            client_tag="STACKED_ONE",
        )

        #
        # Send to Broker
        #

        return self.broker.submit_order(
            request,
        )

    # =====================================================

    @property
    def broker_name(self):

        return self.broker.name

    # =====================================================

    def __str__(self):

        return f"ExecutionEngine({self.broker_name})"

    __repr__ = __str__
