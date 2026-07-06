"""
============================================================

                    STACKED ONE

                ENGINE BRIDGE

------------------------------------------------------------

The only module in the terminal package that imports the
trading engine's internal packages.

Screens call functions defined here - they never construct
engines or import app.analytics / app.strategy / app.execution
/ app.portfolio / app.confluence / app.simulator directly.

============================================================
"""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime

from app.analytics.analytics_manager import AnalyticsManager
from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.execution.execution_engine import ExecutionEngine
from app.execution.paper_broker import PaperBroker
from app.performance.performance_manager import PerformanceManager
from app.performance.strategy_profile import StrategyProfile
from app.pipeline.decision_pipeline import DecisionPipeline
from app.pipeline.market_pipeline import MarketPipeline
from app.portfolio.position import Position
from app.portfolio.position_manager import PositionManager
from app.replay.csv_tick_provider import CSVTickProvider
from app.replay.replay_engine import ReplayEngine
from app.simulator.simulation_config import SimulationConfig
from app.simulator.simulation_result import SimulationResult
from app.simulator.simulation_step import SimulationStep
from app.simulator.simulator import Simulator
from app.strategy.base_strategy import BaseStrategy
from app.strategy.strategy_registry import STRATEGY_REGISTRY

# ==========================================================
# Re-exports (so screens only ever import this module)
# ==========================================================

__all__ = [
    "ALL_STRATEGIES",
    "AnalyticsSnapshot",
    "BaseStrategy",
    "Position",
    "SimulationConfig",
    "SimulationResult",
    "SimulationStep",
    "Simulator",
    "StrategyProfile",
    "build_simulator",
    "load_replay",
    "strategy_classes",
    "strategy_display_names",
    "strategy_classes_by_name",
    "strategy_states",
    "set_strategy_enabled",
    "strategy_scope",
    "timeframes",
]

ALL_STRATEGIES = "All Strategies"


# ==========================================================
# Timeframes
# ==========================================================


def timeframes() -> tuple[str, ...]:

    from app.config.settings import settings

    return tuple(settings.timeframes)


# ==========================================================
# Strategy Registry Access
# ==========================================================


def strategy_classes() -> tuple[type[BaseStrategy], ...]:

    return STRATEGY_REGISTRY


def strategy_display_names() -> tuple[str, ...]:

    return tuple(cls.metadata.name for cls in STRATEGY_REGISTRY)


def strategy_classes_by_name() -> dict[str, type[BaseStrategy]]:

    return {cls.metadata.name: cls for cls in STRATEGY_REGISTRY}


def strategy_states() -> dict[str, bool]:

    return {cls.metadata.name: cls.metadata.enabled for cls in STRATEGY_REGISTRY}


def set_strategy_enabled(
    strategy_cls: type[BaseStrategy],
    enabled: bool,
) -> None:
    """
    Toggles a strategy on/off using the enable mechanism the
    engine already exposes (StrategyMetadata.enabled feeds
    BaseStrategy.can_evaluate(), which StrategyEngine.evaluate()
    already checks). No app/strategy file is touched.
    """

    strategy_cls.metadata = dataclasses.replace(
        strategy_cls.metadata,
        enabled=enabled,
    )


@contextmanager
def strategy_scope(selection: str | None) -> Iterator[None]:
    """
    Temporarily restricts evaluation to a single strategy for
    the duration of one run, restoring the prior enabled/
    disabled configuration (set via the Strategy Laboratory)
    afterwards - regardless of selection being None/ALL_STRATEGIES,
    in which case the current configuration is left untouched.
    """

    previous = strategy_states()

    try:

        if selection and selection != ALL_STRATEGIES:

            for cls in STRATEGY_REGISTRY:

                set_strategy_enabled(
                    cls,
                    cls.metadata.name == selection,
                )

        yield

    finally:

        for cls in STRATEGY_REGISTRY:

            set_strategy_enabled(
                cls,
                previous[cls.metadata.name],
            )


# ==========================================================
# Simulator Construction
# ==========================================================


def build_simulator(csv_path: str) -> Simulator:

    provider = CSVTickProvider(csv_path)

    replay = ReplayEngine(provider)

    return Simulator(
        replay=replay,
        analytics=AnalyticsManager(),
        market=MarketPipeline(),
        decision=DecisionPipeline(),
        execution=ExecutionEngine(broker=PaperBroker()),
        positions=PositionManager(),
        performance=PerformanceManager(),
    )


def load_replay(
    simulator: Simulator,
    symbol: str,
    timeframe: str,
    start: datetime,
    end: datetime,
) -> None:

    simulator.replay.load(
        symbol=symbol,
        timeframe=timeframe,
        start=start,
        end=end,
    )
