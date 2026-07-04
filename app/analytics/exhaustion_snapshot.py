"""
============================================================

                    STACKED ONE

             EXHAUSTION SNAPSHOT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExhaustionSnapshot:

    buyer_exhausted: bool

    seller_exhausted: bool

    confidence: float

    dominant_side: str