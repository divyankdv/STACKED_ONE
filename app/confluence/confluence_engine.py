"""
============================================================

                    STACKED ONE

               CONFLUENCE ENGINE

------------------------------------------------------------

Combines strategy signals into one institutional decision
using weighted confidence aggregation.

============================================================
"""

from __future__ import annotations

from app.confluence.confluence_grade import (
    ConfluenceGrade,
)
from app.confluence.confluence_reason import (
    ConfluenceReason,
)
from app.confluence.confluence_result import (
    ConfluenceResult,
)
from app.strategy.signal_side import SignalSide
from app.strategy.strategy_result import StrategyResult


class ConfluenceEngine:
    """
    Combines multiple strategy signals into one
    institutional trade decision.
    """

    # =====================================================
    # Evaluate
    # =====================================================

    def evaluate(

        self,

        strategy_result: StrategyResult,

    ) -> ConfluenceResult:

        buy_weight = 0.0

        sell_weight = 0.0

        reasons: list[ConfluenceReason] = []

        # -------------------------------------------------
        # Aggregate Strategy Signals
        # -------------------------------------------------

        for signal in strategy_result.signals:

            if signal.side == SignalSide.NEUTRAL:

                continue

            if signal.side == SignalSide.BUY:

                buy_weight += signal.confidence

            elif signal.side == SignalSide.SELL:

                sell_weight += signal.confidence

            reasons.append(

                ConfluenceReason(

                    source=signal.strategy,

                    description=", ".join(signal.reasons),

                    bullish=signal.side == SignalSide.BUY,

                    weight=signal.confidence,

                )

            )

        # -------------------------------------------------
        # Totals
        # -------------------------------------------------

        total_weight = buy_weight + sell_weight

        if total_weight == 0:

            return ConfluenceResult(

                side=SignalSide.NEUTRAL,

                agreement=0.0,

                confidence=0.0,

                grade=ConfluenceGrade.F,

                trade_allowed=False,

                reasons=(),

            )

        # -------------------------------------------------
        # Determine Side
        # -------------------------------------------------

        if buy_weight > sell_weight:

            side = SignalSide.BUY

            dominant = buy_weight

        elif sell_weight > buy_weight:

            side = SignalSide.SELL

            dominant = sell_weight

        else:

            side = SignalSide.NEUTRAL

            dominant = 0.0

        # -------------------------------------------------
        # Metrics
        # -------------------------------------------------

        agreement = dominant / total_weight

        confidence = dominant / max(

            len(strategy_result.signals),

            1,

        )

        # -------------------------------------------------
        # Grade
        # -------------------------------------------------

        if agreement >= 0.90:

            grade = ConfluenceGrade.A_PLUS

        elif agreement >= 0.80:

            grade = ConfluenceGrade.A

        elif agreement >= 0.70:

            grade = ConfluenceGrade.B

        elif agreement >= 0.60:

            grade = ConfluenceGrade.C

        elif agreement >= 0.50:

            grade = ConfluenceGrade.D

        else:

            grade = ConfluenceGrade.F

        # -------------------------------------------------
        # Trade Decision
        # -------------------------------------------------

        trade_allowed = (

            side != SignalSide.NEUTRAL

            and

            agreement >= 0.70

        )

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        return ConfluenceResult(

            side=side,

            agreement=agreement,

            confidence=confidence,

            grade=grade,

            trade_allowed=trade_allowed,

            reasons=tuple(reasons),

        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return "ConfluenceEngine()"

    __repr__ = __str__