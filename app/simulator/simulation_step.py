"""
============================================================

                    STACKED ONE

                SIMULATION STEP

------------------------------------------------------------

Emitted by Simulator.iter_run() after every processed tick.

Gives external observers (progress bars, live dashboards)
a read-only window into the simulation without duplicating
any of its decision-making logic.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.decision.decision_result import DecisionResult
from app.models.candle import Candle
from app.models.tick import Tick
from app.portfolio.position import Position
from app.portfolio.position_update_result import PositionUpdateResult
from app.risk.trade_plan import TradePlan
from app.simulator.exit_engine import ExitDecision
from app.simulator.simulation_result import SimulationResult


@dataclass(slots=True)
class SimulationStep:
    """
    One observed moment of a running simulation.
    """

    # =====================================================
    # Progress
    # =====================================================

    index: int

    total: int

    # =====================================================
    # Market
    # =====================================================

    tick: Tick | None = None

    candle: Candle | None = None

    # =====================================================
    # Decision / Execution
    # =====================================================

    decision: DecisionResult | None = None

    exit_decision: ExitDecision | None = None

    closed_trade: PositionUpdateResult | None = None

    #
    # The TradePlan that opened the position closed_trade
    # refers to. Only set alongside closed_trade.
    #

    entry_plan: TradePlan | None = None

    position: Position | None = None

    # =====================================================
    # Running State
    # =====================================================

    equity: float = 0.0

    #
    # Set only on the final step, once the loop has
    # finished and all statistics are computed.
    #

    result: SimulationResult | None = None

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def progress(self) -> float:

        if self.total <= 0:
            return 1.0

        return min(self.index / self.total, 1.0)

    @property
    def finished(self) -> bool:

        return self.result is not None
