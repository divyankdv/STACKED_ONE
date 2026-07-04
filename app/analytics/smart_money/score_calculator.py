"""
============================================================

                    STACKED ONE

              SCORE CALCULATOR

------------------------------------------------------------

Calculates Smart Money score and confidence from
EvidenceCollection.

============================================================
"""

from __future__ import annotations

from app.analytics.evidence_collection import EvidenceCollection
from app.config.settings import settings


class ScoreCalculator:

    """
    Stateless score calculator.
    """

    @staticmethod
    def calculate(

        evidence: EvidenceCollection,

    ) -> tuple[float, float]:

        #
        # Maximum possible score
        #

        max_score = (

            settings.smart_money_liquidity_weight

            + settings.smart_money_absorption_weight

            + settings.smart_money_iceberg_weight

            + settings.smart_money_large_trade_weight

            + settings.smart_money_exhaustion_weight

            + settings.smart_money_cvd_weight

            + settings.smart_money_pattern_bonus_weight

            + settings.smart_money_hidden_accumulation_weight

            + settings.smart_money_hidden_distribution_weight

        )

        #
        # Institutional score
        #

        score = min(

            evidence.total_weight,

            max_score,

        )

        #
        # Confidence
        #

        confidence = (

            score / max_score

            if max_score > 0

            else 0.0

        )

        return (

            score,

            confidence,

        )