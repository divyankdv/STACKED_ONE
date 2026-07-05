"""
============================================================

                    STACKED ONE

                STRATEGY ENGINE

------------------------------------------------------------

Evaluates every registered trading strategy.

Workflow

CompositeAnalyticsContext
        │
        ▼
Strategy Registry
        │
        ▼
Strategies
        │
        ▼
Signal Ranker
        │
        ▼
Strategy Result

============================================================
"""

from __future__ import annotations

from collections.abc import Iterator

from app.analytics.composite_context import (
    CompositeAnalyticsContext,
)
from app.strategy.base_strategy import (
    BaseStrategy,
)
from app.strategy.signal_ranker import (
    SignalRanker,
)
from app.strategy.strategy_registry import (
    STRATEGY_REGISTRY,
)
from app.strategy.strategy_result import (
    StrategyResult,
)
from app.strategy.strategy_signal import (
    StrategySignal,
)


class StrategyEngine:
    """
    Evaluates every registered strategy and returns
    an immutable StrategyResult.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self) -> None:

        self._strategies: tuple[BaseStrategy, ...] = tuple(
            strategy()
            for strategy in STRATEGY_REGISTRY
        )

    # =====================================================
    # Properties
    # =====================================================

    @property
    def strategies(self) -> tuple[BaseStrategy, ...]:
        return self._strategies

    @property
    def strategy_count(self) -> int:
        return len(self._strategies)

    # =====================================================
    # Evaluate
    # =====================================================

    def evaluate(
        self,
        context: CompositeAnalyticsContext,
    ) -> StrategyResult:

        signal_list: list[StrategySignal] = []

        for strategy in self._strategies:

            if not strategy.can_evaluate(context):
                continue

            signal = strategy.evaluate(context)

            signal_list.append(signal)

        signals: tuple[StrategySignal, ...] = tuple(signal_list)

        best_signal = SignalRanker.rank(signals)

        return StrategyResult(
            signals=signals,
            best_signal=best_signal,
        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:

        for strategy in self._strategies:
            strategy.reset()

    # =====================================================
    # Strategy Lookup
    # =====================================================

    def get_strategy(
        self,
        name: str,
    ) -> BaseStrategy | None:

        for strategy in self._strategies:

            if strategy.name == name:
                return strategy

        return None

    # =====================================================
    # Enabled Strategies
    # =====================================================

    def enabled_strategies(
        self,
    ) -> tuple[BaseStrategy, ...]:

        return tuple(
            strategy
            for strategy in self._strategies
            if strategy.enabled
        )

    # =====================================================
    # Disabled Strategies
    # =====================================================

    def disabled_strategies(
        self,
    ) -> tuple[BaseStrategy, ...]:

        return tuple(
            strategy
            for strategy in self._strategies
            if not strategy.enabled
        )

    # =====================================================
    # Magic Methods
    # =====================================================

    def __len__(self) -> int:
        return len(self._strategies)

    def __iter__(self) -> Iterator[BaseStrategy]:
        return iter(self._strategies)

    def __str__(self) -> str:
        return (
            "StrategyEngine("
            f"strategies={self.strategy_count}"
            ")"
        )

    __repr__ = __str__