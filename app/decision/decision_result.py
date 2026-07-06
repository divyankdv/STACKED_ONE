"""
============================================================

                    STACKED ONE

                DECISION RESULT

------------------------------------------------------------

Final output of the Decision Pipeline.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.analytics.analytics_snapshot import AnalyticsSnapshot
from app.confluence.confluence_result import ConfluenceResult
from app.risk.trade_plan import TradePlan


@dataclass(slots=True)
class DecisionResult:
    #
    # Pipeline Outputs
    #

    analytics: AnalyticsSnapshot

    composite: object

    strategy: object

    confluence: ConfluenceResult

    trade_plan: TradePlan

    # =====================================================

    @property
    def executable(self) -> bool:
        return self.trade_plan.approved
