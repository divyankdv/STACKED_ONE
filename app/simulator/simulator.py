"""
============================================================

                    STACKED ONE

                    SIMULATOR

============================================================
"""

from __future__ import annotations

from collections.abc import Iterator

from app.analytics.analytics_manager import AnalyticsManager
from app.execution.execution_engine import ExecutionEngine
from app.performance.performance_manager import PerformanceManager
from app.pipeline.decision_pipeline import DecisionPipeline
from app.pipeline.market_pipeline import MarketPipeline
from app.portfolio.position_manager import PositionManager
from app.replay.replay_engine import ReplayEngine
from app.risk.trade_plan import TradePlan
from app.simulator.exit_engine import ExitEngine
from app.simulator.paper_execution import PaperExecution
from app.simulator.simulation_config import SimulationConfig
from app.simulator.simulation_result import SimulationResult
from app.simulator.simulation_step import SimulationStep


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
        self.paper_execution = PaperExecution()

        #
        # Tracks the TradePlan that opened each symbol's
        # current position, so strategy/RR information
        # survives from entry until exit.
        #

        self._open_plans: dict[str, TradePlan] = {}

    # =====================================================
    # Run (Batch)
    # =====================================================

    def run(
        self,
        config: SimulationConfig,
    ) -> SimulationResult:
        """
        Runs the simulation to completion and returns the
        final SimulationResult.

        Thin wrapper around iter_run() - identical behavior
        to a plain batch run.
        """

        result: SimulationResult | None = None

        for step in self.iter_run(config):

            if step.result is not None:
                result = step.result

        assert result is not None

        return result

    # =====================================================
    # Run (Observable)
    # =====================================================

    def iter_run(
        self,
        config: SimulationConfig,
    ) -> Iterator[SimulationStep]:
        """
        Same simulation as run(), but yields a SimulationStep
        after every processed tick so external observers
        (progress bars, live dashboards) can watch it unfold
        without re-implementing any of its logic.

        The final yielded step carries the completed
        SimulationResult.
        """

        self.reset()

        #
        # Running Statistics
        #

        equity = config.initial_capital

        equity_curve: list[float] = [equity]

        total_trades = 0

        winning_trades = 0

        losing_trades = 0

        breakeven_trades = 0

        gross_profit = 0.0

        gross_loss = 0.0

        trade_ids: list[str] = []

        pnls: list[float] = []

        total_ticks = len(self.replay.provider)

        #
        # Main Replay Loop
        #

        for index, tick in enumerate(self.replay, start=1):
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

                yield SimulationStep(
                    index=index,
                    total=total_ticks,
                    tick=tick,
                    equity=equity,
                )

                continue

            candle = candles.get(
                config.timeframe,
            )

            if candle is None:

                yield SimulationStep(
                    index=index,
                    total=total_ticks,
                    tick=tick,
                    equity=equity,
                )

                continue

            #
            # Existing Position?
            #

            position = self.positions.current_position

            exit_decision = None

            if position is not None:

                exit_decision = self.exit_engine.evaluate(

                    position,

                    candle,

                )

                if exit_decision.closed:

                    #
                    # Create closing ExecutionReport
                    #

                    closing_report = self.paper_execution.close_position(
                        position,
                        exit_decision.exit_price,
                    )

                    #
                    # Feed PositionManager
                    #

                    update = self.positions.process_execution(
                        closing_report,
                    )

                    #
                    # Record Performance
                    #

                    trade_plan = self._open_plans.pop(
                        position.symbol,
                        None,
                    )

                    if trade_plan is not None:

                        self.performance.record_trade(
                            strategy_name=trade_plan.strategy,
                            pnl=update.realized_pnl,
                            rr=trade_plan.risk_reward,
                        )

                    #
                    # Statistics
                    #

                    realized_pnl = update.realized_pnl

                    total_trades += 1

                    if realized_pnl > 0:

                        winning_trades += 1

                        gross_profit += realized_pnl

                    elif realized_pnl < 0:

                        losing_trades += 1

                        gross_loss += abs(realized_pnl)

                    else:

                        breakeven_trades += 1

                    equity += realized_pnl

                    equity_curve.append(equity)

                    trade_ids.append(closing_report.execution_id)

                    pnls.append(realized_pnl)

                    yield SimulationStep(
                        index=index,
                        total=total_ticks,
                        tick=tick,
                        candle=candle,
                        exit_decision=exit_decision,
                        closed_trade=update,
                        entry_plan=trade_plan,
                        position=self.positions.current_position,
                        equity=equity,
                    )

                    continue

            #
            # Decision
            #

            decision = self.decision.process(
                analytics=self.analytics.snapshot(),
                entry_price=tick.price,
            )

            trade_plan = decision.trade_plan

            if not trade_plan.rejected:

                #
                # Execution
                #

                report = self.execution.execute(
                    trade_plan,
                )

                if report is not None:

                    #
                    # Position Manager
                    #

                    self.positions.process_execution(
                        report,
                    )

                    self._open_plans[report.symbol] = trade_plan

            yield SimulationStep(
                index=index,
                total=total_ticks,
                tick=tick,
                candle=candle,
                decision=decision,
                exit_decision=exit_decision,
                position=self.positions.current_position,
                equity=equity,
            )

        #
        # Final Statistics
        #

        net_profit = gross_profit - gross_loss

        win_rate = (
            winning_trades / total_trades
            if total_trades > 0
            else 0.0
        )

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else 0.0
        )

        expectancy = (
            net_profit / total_trades
            if total_trades > 0
            else 0.0
        )

        peak = equity_curve[0]

        max_drawdown = 0.0

        for value in equity_curve:

            peak = max(peak, value)

            max_drawdown = max(max_drawdown, peak - value)

        if len(pnls) > 1:

            mean_pnl = sum(pnls) / len(pnls)

            variance = sum((p - mean_pnl) ** 2 for p in pnls) / len(pnls)

            stdev = variance ** 0.5

            sharpe_ratio = mean_pnl / stdev if stdev > 0 else 0.0

        else:

            sharpe_ratio = 0.0

        final_result = SimulationResult(
            strategy=config.strategy,
            symbol=config.symbol,
            timeframe=config.timeframe,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            breakeven_trades=breakeven_trades,
            net_profit=net_profit,
            gross_profit=gross_profit,
            gross_loss=gross_loss,
            win_rate=win_rate,
            profit_factor=profit_factor,
            expectancy=expectancy,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            ending_equity=equity,
            equity_curve=equity_curve,
            trades=trade_ids,
        )

        yield SimulationStep(
            index=total_ticks,
            total=total_ticks,
            equity=equity,
            result=final_result,
        )

    # =====================================================

    def reset(self):

        self.analytics.reset()

        self.market.reset()

        self.positions.reset()

        self.performance.reset()

        self.decision.reset()

        self._open_plans.clear()

    # =====================================================

    def __str__(self):

        return "Simulator()"

    __repr__ = __str__
