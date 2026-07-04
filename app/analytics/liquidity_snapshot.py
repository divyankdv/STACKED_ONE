"""
============================================================

                    STACKED ONE

              LIQUIDITY SNAPSHOT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LiquiditySnapshot:

    score: float

    state: str

    absorption: bool

    iceberg: bool

    institutional_activity: bool

    confidence: float