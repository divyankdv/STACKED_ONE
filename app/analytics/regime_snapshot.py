"""
============================================================

                    STACKED ONE

                REGIME SNAPSHOT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.analytics.evidence import Evidence
from app.analytics.market_regime import MarketRegime


@dataclass(frozen=True, slots=True)
class RegimeSnapshot:

    #
    # Current Market Regime
    #

    regime: MarketRegime

    #
    # Strength
    #

    strength: float

    confidence: float

    #
    # Participation
    #

    participation: str

    #
    # Explainability
    #

    evidence: tuple[Evidence, ...]