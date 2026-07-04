"""
============================================================

                    STACKED ONE

                  BASE STRATEGY

------------------------------------------------------------

Abstract base class for every trading strategy.

Every strategy receives a CompositeAnalyticsContext
and returns a StrategySignal.

============================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.analytics.composite_context import (
    CompositeAnalyticsContext,
)

from app.strategy.strategy_signal import (
    StrategySignal,
)

from app.strategy.strategy_metadata import (
    StrategyMetadata,
)


class BaseStrategy(ABC):
    """
    Base class for all trading strategies.
    """

    # =====================================================
    # Metadata
    # =====================================================

    metadata = StrategyMetadata(

        name="Base Strategy",

        description="Abstract base strategy.",

        version="1.0",

        category="General",

        timeframe="Any",

    )

    # =====================================================
    # Evaluate
    # =====================================================

    @abstractmethod
    def evaluate(

        self,

        context: CompositeAnalyticsContext,

    ) -> StrategySignal:
        """
        Evaluate the current market state and return a signal.
        """

        raise NotImplementedError

    # =====================================================
    # Can Evaluate
    # =====================================================

    def can_evaluate(

        self,

        context: CompositeAnalyticsContext,

    ) -> bool:
        """
        Override if the strategy has prerequisites.

        Example:
            - Liquidity available
            - Market open
            - Session active
        """

        return self.metadata.enabled

    # =====================================================
    # Reset
    # =====================================================

    def reset(self) -> None:
        """
        Override if the strategy maintains internal state.
        """

        pass

    # =====================================================
    # Convenience Properties
    # =====================================================

    @property
    def name(self) -> str:

        return self.metadata.name

    @property
    def description(self) -> str:

        return self.metadata.description

    @property
    def version(self) -> str:

        return self.metadata.version

    @property
    def category(self) -> str:

        return self.metadata.category

    @property
    def timeframe(self) -> str:

        return self.metadata.timeframe

    @property
    def author(self) -> str:

        return self.metadata.author

    @property
    def enabled(self) -> bool:

        return self.metadata.enabled

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            f"{self.__class__.__name__}"

            f"(name={self.name}, "

            f"version={self.version}, "

            f"enabled={self.enabled})"

        )

    __repr__ = __str__