"""
============================================================

                    STACKED ONE

                DECISION RECORD

------------------------------------------------------------

Stores one decision produced by the Confluence Engine.

Every decision is recorded whether or not a trade
is eventually executed.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.confluence.confluence_grade import ConfluenceGrade
from app.strategy.signal_side import SignalSide


@dataclass(slots=True)
class DecisionRecord:

    #
    # Timestamp
    #

    timestamp: datetime

    #
    # Instrument
    #

    symbol: str

    #
    # Decision
    #

    side: SignalSide

    #
    # Confluence
    #

    confidence: float

    agreement: float

    grade: ConfluenceGrade

    #
    # Risk
    #

    trade_allowed: bool

    #
    # Optional Outcome
    #

    executed: bool = False

    pnl: float | None = None

    #
    # Supporting Information
    #

    strategy_names: tuple[str, ...] = field(

        default_factory=tuple,

    )

    reasons: tuple[str, ...] = field(

        default_factory=tuple,

    )

    # =====================================================

    @property
    def profitable(self):

        return (

            self.pnl is not None

            and

            self.pnl > 0

        )

    # =====================================================

    def __str__(self):

        return (

            "DecisionRecord("

            f"{self.symbol}, "

            f"{self.side.value}, "

            f"{self.grade.value}, "

            f"{self.confidence:.2f}"

            ")"

        )

    __repr__ = __str__