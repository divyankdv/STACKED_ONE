"""
============================================================

                    STACKED ONE

               ICEBERG SNAPSHOT

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IcebergSnapshot:

    active: bool

    side: str

    price: float

    absorbed_volume: float

    trade_count: int

    confidence: float