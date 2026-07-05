"""
============================================================

                    STACKED ONE

                POSITION MANAGER

------------------------------------------------------------

Maintains all open portfolio positions.

Responsibilities

✓ Open positions
✓ Increase positions
✓ Reduce positions
✓ Flip positions
✓ Close positions
✓ Mark-to-market
✓ Portfolio statistics

============================================================
"""

from __future__ import annotations

from copy import deepcopy

from app.execution.execution_report import ExecutionReport
from app.portfolio.position import Position
from app.portfolio.position_update_result import PositionUpdateResult


class PositionManager:
    """
    Portfolio position manager.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self._positions: dict[str, Position] = {}

    # =====================================================
    # Process Execution
    # =====================================================

    def process_execution(
        self,
        report: ExecutionReport,
    ) -> PositionUpdateResult:

        symbol = report.symbol

        #
        # First Position
        #

        if symbol not in self._positions:

            position = Position(

                symbol=symbol,

                side=report.side,

            )

            position.add_execution(report)

            self._positions[symbol] = position

            return PositionUpdateResult(

                current_position=position,

                opened_new_position=True,

            )

        position = self._positions[symbol]

        previous = deepcopy(position)

        #
        # Same Direction
        #

        if position.side == report.side:

            position.add_execution(report)

            return PositionUpdateResult(

                previous_position=previous,

                current_position=position,

            )

        #
        # Opposite Direction
        #

        return self._reduce_or_flip(

            position,

            report,

            previous,

        )
    
        # =====================================================
    # Reduce / Flip
    # =====================================================

    def _reduce_or_flip(
        self,
        position: Position,
        report: ExecutionReport,
        previous: Position,
    ) -> PositionUpdateResult:

        #
        # Reduce the current position
        #

        reduction = position.reduce(report)

        #
        # Fully closed with no flip
        #

        if reduction.position_closed and not reduction.position_flipped:

            self._positions.pop(position.symbol, None)

            return PositionUpdateResult(

                previous_position=previous,

                closed_position=position,

                closed_existing_position=True,

                realized_pnl=reduction.realized_pnl,

            )

        #
        # Partial reduction
        #

        if not reduction.position_flipped:

            return PositionUpdateResult(

                previous_position=previous,

                current_position=position,

                realized_pnl=reduction.realized_pnl,

            )

        #
        # Position Flip
        #

        return self._flip_position(

            position,

            report,

            reduction,

            previous,

        )
    
    # =====================================================
    # Flip Position
    # =====================================================

    def _flip_position(
        self,
        old_position: Position,
        report: ExecutionReport,
        reduction,
        previous: Position,
    ) -> PositionUpdateResult:

        #
        # Remove old position
        #

        self._positions.pop(

            old_position.symbol,

            None,

        )

        #
        # Create execution report for remaining quantity
        #

        flipped_report = ExecutionReport(

            order_id=report.order_id,

            exchange_order_id=report.exchange_order_id,

            execution_id=report.execution_id,

            symbol=report.symbol,

            side=report.side,

            requested_quantity=reduction.remaining_quantity,

            requested_price=report.requested_price,

            executed_quantity=reduction.remaining_quantity,

            executed_price=report.executed_price,

            status=report.status,

            commission=0.0,

            fees=0.0,

            executed_at=report.executed_at,

            broker=report.broker,

            message="Position Flip",

        )

        #
        # Open opposite position
        #

        new_position = Position(

            symbol=report.symbol,

            side=report.side,

        )

        new_position.add_execution(

            flipped_report,

        )

        self._positions[

            report.symbol

        ] = new_position

        return PositionUpdateResult(

            previous_position=previous,

            closed_position=old_position,

            current_position=new_position,

            closed_existing_position=True,

            opened_new_position=True,

            position_flipped=True,

            realized_pnl=reduction.realized_pnl,

        )
    
        # =====================================================
    # Mark To Market
    # =====================================================

    def mark_to_market(
        self,
        symbol: str,
        market_price: float,
    ) -> float:

        position = self._positions.get(symbol)

        if position is None:
            return 0.0

        return position.mark_to_market(
            market_price,
        )

    # =====================================================
    # Lookup
    # =====================================================

    def get(
        self,
        symbol: str,
    ) -> Position | None:

        return self._positions.get(symbol)

    # =====================================================
    # Remove
    # =====================================================

    def remove(
        self,
        symbol: str,
    ) -> None:

        self._positions.pop(symbol, None)

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        symbol: str,
    ) -> bool:

        return symbol in self._positions

    # =====================================================
    # Portfolio
    # =====================================================

    @property
    def positions(self) -> tuple[Position, ...]:

        return tuple(
            self._positions.values()
        )

    @property
    def symbols(self) -> tuple[str, ...]:

        return tuple(
            self._positions.keys()
        )

    @property
    def position_count(self) -> int:

        return len(self._positions)

    # =====================================================
    # Portfolio Statistics
    # =====================================================

    @property
    def total_realized_pnl(self) -> float:

        return sum(

            p.realized_pnl

            for p in self._positions.values()

        )

    @property
    def total_unrealized_pnl(self) -> float:

        return sum(

            p.unrealized_pnl

            for p in self._positions.values()

        )

    @property
    def total_commission(self) -> float:

        return sum(

            p.commission

            for p in self._positions.values()

        )

    @property
    def total_fees(self) -> float:

        return sum(

            p.fees

            for p in self._positions.values()

        )

    @property
    def total_cost(self) -> float:

        return (

            self.total_commission

            +

            self.total_fees

        )

    @property
    def net_pnl(self) -> float:

        return (

            self.total_realized_pnl

            +

            self.total_unrealized_pnl

            -

            self.total_cost

        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self):

        self._positions.clear()

    # =====================================================
    # String
    # =====================================================

    def __len__(self):

        return self.position_count

    def __str__(self):

        return (

            "PositionManager("

            f"positions={self.position_count}, "

            f"net_pnl={self.net_pnl:.2f}"

            ")"

        )

    __repr__ = __str__