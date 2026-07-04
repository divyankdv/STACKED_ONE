"""
============================================================

                    STACKED ONE

             SMART MONEY SNAPSHOT

------------------------------------------------------------

Represents inferred institutional activity.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from app.analytics.evidence import Evidence


@dataclass(frozen=True, slots=True)
class SmartMoneySnapshot:

    # =====================================================
    # Market Bias
    # =====================================================

    bias: str

    # =====================================================
    # Institutional State
    # =====================================================

    accumulating: bool

    distributing: bool

    institutional_score: float

    confidence: float

    # =====================================================
    # Evidence
    # =====================================================

    evidence: tuple[Evidence, ...]