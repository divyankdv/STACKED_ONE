"""
============================================================

                    STACKED ONE

                    SIMULATOR

============================================================
"""

from __future__ import annotations

from app.analytics.analytics_manager import AnalyticsManager
from app.pipeline.decision_pipeline import DecisionPipeline
from app.execution.execution_engine import ExecutionEngine
from app.performance.performance_manager import PerformanceManager
from app.pipeline.market_pipeline import MarketPipeline
from app.portfolio.position_manager import PositionManager
from app.replay.replay_engine import ReplayEngine
from app.simulator.simulation_config import SimulationConfig
from app.simulator.simulation_result import SimulationResult
from app.simulator.exit_engine import ExitEngine


class Simulator:
    def __init__(
        self,
        replay: ReplayEngine,
        analytics: AnalyticsManager,
        market: MarketPipeline,
        decision: DecisionPipeline,
        execution: ExecutionEngine,
        positions: PositionManager,
        performance: PerformanceManager,
    ) -> None:

        self.replay = replay
        self.analytics = analytics
        self.market = market
        self.decision = decision
        self.execution = execution
        self.positions = positions
        self.performance = performance
        self.exit_engine = ExitEngine()

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
            ending_equity=config.initial_capital,
        )

        #
        # Main Replay Loop
        #

        for tick in self.replay:
            #
            # Analytics
            #

            self.analytics.update_trade(
                tick,
            )

            #
            # Market
            #

            candles = self.market.process_tick(
                tick,
            )

            if candles is None:
                continue

            candle = candles.get(
                config.timeframe,
            )

            if candle is None:
                continue

            #
            # Existing Position?
            #

            position = self.positions.current_position

            if position is not None:

                exit_decision = self.exit_engine.evaluate(

                    position,

                )

                if exit_decision.closed:

                    #
                    # TODO
                    # Create closing ExecutionReport
                    #

                    #
                    # TODO
                    # Feed PositionManager
                    #

                    #
                    # TODO
                    # Record Performance
                    #

                    continue

            #
            # Decision
            #

            decision = self.decision.process(
                analytics=self.analytics.snapshot(),
                entry_price=tick.price,
            )

            trade_plan = decision.trade_plan

            if trade_plan.rejected:
                continue

            #
            # TODO
            # Execution
            #

            #
            # TODO
            # Position Manager
            #

            #
            # TODO
            # Performance
            #

        return result

    # =====================================================

    def reset(self):

        self.analytics.reset()

        self.market.reset()

        self.positions.reset()

        self.performance.reset()

        self.decision.reset()

    # =====================================================

    def __str__(self):

        return "Simulator()"

    __repr__ = __str__
