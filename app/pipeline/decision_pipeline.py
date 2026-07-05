"""
============================================================

                    STACKED ONE

                DECISION PIPELINE

------------------------------------------------------------

Transforms market state into a trading decision.

Pipeline

Analytics
    ↓
Composite
    ↓
Strategies
    ↓
Confluence
    ↓
Journal
    ↓
Performance
    ↓
Risk
    ↓
Execution

============================================================
"""

from __future__ import annotations

from app.analytics.analytics_manager import AnalyticsManager
from app.analytics.composite_analytics_manager import (
    CompositeAnalyticsManager,
)
from app.confluence.confluence_engine import (
    ConfluenceEngine,
)
from app.performance.performance_manager import (
    PerformanceManager,
)
from app.strategy.strategy_engine import (
    StrategyEngine,
)

# These will be implemented next
# from app.journal.journal_manager import JournalManager
# from app.risk.risk_engine import RiskEngine
# from app.execution.execution_engine import ExecutionEngine


class DecisionPipeline:

    """
    Central trading decision orchestrator.
    """

    # =====================================================

    def __init__(self):

        self.analytics = AnalyticsManager()

        self.composite = CompositeAnalyticsManager()

        self.strategy = StrategyEngine()

        self.confluence = ConfluenceEngine()

        self.performance = PerformanceManager()

        #
        # Coming next
        #

        self.journal = None

        self.risk = None

        self.execution = None

    # =====================================================

    def process_trade(

        self,

        trade,

    ):

        """
        Processes one trade through the entire
        decision pipeline.
        """

        #
        # Primary Analytics
        #

        analytics = self.analytics.update(

            trade,

        )

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
        # Journal
        #

        if self.journal is not None:

            self.journal.record(

                analytics,

                composite,

                strategy_result,

                confluence,

            )

        #
        # Performance Observation
        #

        # Performance updates after completed trades,
        # so nothing is recorded here yet.

        #
        # Risk
        #

        risk_result = None

        if self.risk is not None:

            risk_result = self.risk.evaluate(

                confluence,

            )

        #
        # Execution
        #

        execution_result = None

        if (

            self.execution is not None

            and

            risk_result is not None

        ):

            execution_result = self.execution.execute(

                risk_result,

            )

        return {

            "analytics": analytics,

            "composite": composite,

            "strategy": strategy_result,

            "confluence": confluence,

            "risk": risk_result,

            "execution": execution_result,

        }

    # =====================================================

    def reset(self):

        self.analytics.reset()

        self.composite.reset()

        self.strategy.reset()

    # =====================================================

    def __str__(self):

        return "DecisionPipeline()"

    __repr__ = __str__