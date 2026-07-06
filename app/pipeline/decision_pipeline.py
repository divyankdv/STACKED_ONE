"""
============================================================

                    STACKED ONE

                DECISION PIPELINE

------------------------------------------------------------

Transforms analytics into an executable TradePlan.

Pipeline

Analytics
    ↓
Composite
    ↓
Strategies
    ↓
Confluence
    ↓
Risk
    ↓
Trade Plan

============================================================
"""

from __future__ import annotations

from app.analytics.composite_analytics_manager import (
    CompositeAnalyticsManager,
)
from app.confluence.confluence_engine import (
    ConfluenceEngine,
)
from app.decision.decision_result import DecisionResult
from app.risk.risk_engine import RiskEngine
from app.strategy.strategy_engine import StrategyEngine


class DecisionPipeline:
    """
    Central trading decision orchestrator.
    """

    # =====================================================

    def __init__(self):

        self.composite = CompositeAnalyticsManager()

        self.strategy = StrategyEngine()

        self.confluence = ConfluenceEngine()

        self.risk = RiskEngine()

        self.journal = None

    # =====================================================

    def process(
        self,
        analytics,
        entry_price: float,
    ) -> DecisionResult:
        """
        Produce a TradePlan from an AnalyticsSnapshot.
        """

        #
        # Composite Analytics
        #

        composite = self.composite.update(
            analytics,
        )

        #
        # Strategy Evaluation
        #

        strategy_result = self.strategy.evaluate(
            composite,
        )

        #
        # Confluence
        #

        confluence = self.confluence.evaluate(
            strategy_result,
        )

        #
        # Optional Journal
        #

        if self.journal is not None:
            self.journal.record(
                analytics,
                composite,
                strategy_result,
                confluence,
            )

        #
        # Risk Evaluation
        #

        trade_plan = self.risk.evaluate(
            composite=composite,
            strategy=strategy_result,
            confluence=confluence,
            entry_price=entry_price,
        )

        #
        # Final Result
        #

        return DecisionResult(
            analytics=analytics,
            composite=composite,
            strategy=strategy_result,
            confluence=confluence,
            trade_plan=trade_plan,
        )

    # =====================================================

    def reset(self):

        self.composite.reset()

        self.strategy.reset()

        self.risk.reset()

    # =====================================================

    def __str__(self):

        return "DecisionPipeline()"

    __repr__ = __str__
