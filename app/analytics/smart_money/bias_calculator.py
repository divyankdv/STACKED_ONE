"""
============================================================

                    STACKED ONE

               BIAS CALCULATOR

------------------------------------------------------------

Determines Smart Money market bias from
EvidenceCollection and institutional score.

============================================================
"""

from __future__ import annotations

from app.analytics.evidence_collection import EvidenceCollection
from app.analytics.smart_money_bias import SmartMoneyBias
from app.config.settings import settings


class BiasCalculator:

    """
    Stateless bias calculator.
    """

    @staticmethod
    def calculate(

        evidence: EvidenceCollection,

        score: float,

    ) -> SmartMoneyBias:

        #
        # Below threshold
        #

        if score < settings.smart_money_bias_threshold:

            return SmartMoneyBias.NEUTRAL

        bullish = evidence.bullish_weight

        bearish = evidence.bearish_weight

        #
        # Bullish dominance
        #

        if bullish > bearish:

            return SmartMoneyBias.LONG

        #
        # Bearish dominance
        #

        if bearish > bullish:

            return SmartMoneyBias.SHORT

        #
        # Equal conviction
        #

        return SmartMoneyBias.NEUTRAL