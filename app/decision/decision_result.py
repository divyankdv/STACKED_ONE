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


@dataclass(slots=True)
class DecisionResult:
    #
    # Pipeline Outputs
    #

    analytics: AnalyticsSnapshot

    composite: object

    strategy: object

    confluence: ConfluenceResult

    risk: object | None

    execution: object | None

    # =====================================================

    @property
    def executable(self) -> bool:

        return self.risk is not None
