"""
============================================================

                    STACKED ONE

                 EVIDENCE MODEL

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Evidence:

    category: str

    description: str

    weight: float

    bullish: bool