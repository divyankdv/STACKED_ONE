"""
============================================================

                    STACKED ONE

               STRATEGY REGISTRY

------------------------------------------------------------

Registers every trading strategy available to the
Strategy Engine.

Every strategy should inherit from BaseStrategy.

============================================================
"""

from __future__ import annotations

from app.strategy.base_strategy import BaseStrategy
from app.strategy.strategies.accumulation_strategy import (
    AccumulationStrategy,
)
from app.strategy.strategies.breakout_strategy import (
    BreakoutStrategy,
)
from app.strategy.strategies.distribution_strategy import (
    DistributionStrategy,
)
from app.strategy.strategies.reversal_strategy import (
    ReversalStrategy,
)

# ==========================================================
# Strategy Registry
# ==========================================================

STRATEGY_REGISTRY: tuple[type[BaseStrategy], ...] = (
    #
    # Institutional Strategies
    #
    AccumulationStrategy,
    DistributionStrategy,
    #
    # Momentum Strategy
    #
    BreakoutStrategy,
    #
    # Mean Reversion Strategy
    #
    ReversalStrategy,
)


# ==========================================================
# Registry Helpers
# ==========================================================


def strategy_count() -> int:
    """
    Total number of registered strategies.
    """

    return len(
        STRATEGY_REGISTRY,
    )


def strategy_names() -> tuple[str, ...]:
    """
    Returns strategy class names.
    """

    return tuple(strategy.__name__ for strategy in STRATEGY_REGISTRY)


def create_strategies() -> tuple[BaseStrategy, ...]:
    """
    Instantiates every registered strategy.
    """

    return tuple(strategy() for strategy in STRATEGY_REGISTRY)


# ==========================================================
# String
# ==========================================================


def __str__():

    return f"StrategyRegistry({strategy_count()} strategies)"
