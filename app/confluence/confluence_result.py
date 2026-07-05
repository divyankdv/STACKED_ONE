"""
============================================================

                    STACKED ONE

              CONFLUENCE RESULT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.confluence.confluence_grade import (
    ConfluenceGrade,
)
from app.confluence.confluence_reason import (
    ConfluenceReason,
)
from app.strategy.signal_side import SignalSide


@dataclass(slots=True)
class ConfluenceResult:

    #
    # Final Decision
    #

    side: SignalSide

    #
    # Agreement (0-1)
    #

    agreement: float

    #
    # Confidence
    #

    confidence: float

    #
    # Trade Quality
    #

    grade: ConfluenceGrade

    #
    # Can we trade?
    #

    trade_allowed: bool

    #
    # Supporting Reasons
    #

    reasons: tuple[ConfluenceReason, ...] = field(

        default_factory=tuple,

    )

    # =====================================================

    @property
    def reason_count(self):

        return len(

            self.reasons,

        )

    # =====================================================

    def __str__(self):

        return (

            "ConfluenceResult("

            f"side={self.side.value}, "

            f"grade={self.grade.value}, "

            f"agreement={self.agreement:.2f}, "

            f"confidence={self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__