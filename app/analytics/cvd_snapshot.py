"""
============================================================

                    STACKED ONE

                    CVD SNAPSHOT

------------------------------------------------------------

Immutable state of the Cumulative Volume Delta engine.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CVDSnapshot:

    current: float

    highest: float

    lowest: float

    session_open: float

    trade_count: int