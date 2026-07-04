"""
============================================================

                    STACKED ONE

               DECISION CONTEXT

------------------------------------------------------------

Immutable snapshot of the complete decision state.

Every decision references one DecisionContext.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.analytics.composite_context import CompositeAnalyticsContext

from app.strategy.strategy_result import StrategyResult

from app.confluence.confluence_result import (
    ConfluenceResult,
)


@dataclass(slots=True, frozen=True)
class DecisionContext:
    """
    Complete market decision snapshot.
    """

    #
    # Market
    #

    analytics: AnalyticsSnapshot

    composite: CompositeAnalyticsContext

    #
    # Strategy
    #

    strategy: StrategyResult

    #
    # Final Decision
    #

    confluence: ConfluenceResult

    # =====================================================

    def __str__(self):

        return (

            "DecisionContext("

            f"strategies={self.strategy.strategy_count}, "

            f"side={self.confluence.side.value}, "

            f"confidence={self.confluence.confidence:.2f}"

            ")"

        )

    __repr__ = __str__