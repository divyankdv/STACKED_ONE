"""
============================================================

                    STACKED ONE

                    SIMULATOR

------------------------------------------------------------

Coordinates complete historical simulations.

Responsibilities

✓ Replay historical market data
✓ Feed Market Pipeline
✓ Evaluate trading strategy
✓ Execute approved trades
✓ Update portfolio
✓ Collect performance statistics

============================================================
"""

from __future__ import annotations

from app.execution.execution_engine import ExecutionEngine
from app.performance.performance_manager import PerformanceManager
from app.pipeline.market_pipeline import MarketPipeline
from app.portfolio.position_manager import PositionManager
from app.replay.replay_engine import ReplayEngine
from app.simulator.simulation_config import SimulationConfig
from app.simulator.simulation_result import SimulationResult
from app.strategy.strategy import Strategy


class Simulator:
    """
    Historical market simulator.

    The simulator itself contains no trading logic.
    It simply coordinates all subsystems.
    """

    def __init__(
        self,
        replay: ReplayEngine,
        market: MarketPipeline,
        strategy: Strategy,
        execution: ExecutionEngine,
        positions: PositionManager,
        performance: PerformanceManager,
    ) -> None:

        self.replay = replay
        self.market = market
        self.strategy = strategy
        self.execution = execution
        self.positions = positions
        self.performance = performance

    # =====================================================
    # Run Simulation
    # =====================================================

    def run(
        self,
        config: SimulationConfig,
    ) -> SimulationResult:

        self.reset()

        result = SimulationResult(
            strategy=config.strategy,
            symbol=config.symbol,
            timeframe=config.timeframe,
        )

        #
        # ==================================================
        # Main Replay Loop
        # ==================================================
        #

        for replay_event in self.replay:

            #
            # Phase 1
            # Feed market pipeline
            #

            completed = self.market.process_tick(
                replay_event.tick,
            )

            if completed is None:
                continue

            #
            # Phase 2
            # Strategy evaluation
            #

            trade_plan = self.strategy.evaluate(
                completed,
            )

            if trade_plan is None:
                continue

            if trade_plan.rejected:
                continue

            #
            # Phase 3
            # Execute trade
            #

            # execution_result = self.execution.execute(...)

            #
            # Phase 4
            # Update positions
            #

            # self.positions.process_execution(...)

            #
            # Phase 5
            # Update performance
            #

            # self.performance.update(...)

        #
        # ==================================================
        # Collect Statistics
        # ==================================================
        #

        result.total_trades = 0

        result.winning_trades = 0

        result.losing_trades = 0

        result.net_profit = 0.0

        result.ending_equity = config.initial_capital

        return result

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:

        self.market.reset()

        self.positions.reset()

        self.performance.reset()

    # =====================================================
    # String
    # =====================================================

    def __str__(self) -> str:

        return (
            "Simulator("
            f"strategy={self.strategy.name}"
            ")"
        )

    __repr__ = __str__