"""
============================================================

                    STACKED ONE

              ABSORPTION SNAPSHOT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AbsorptionSnapshot:

    bullish_score: float

    bearish_score: float

    active: bool

    absorbed_volume: float

    duration_seconds: float

    last_price: float