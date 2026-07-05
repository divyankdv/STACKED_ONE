"""
============================================================

                    STACKED ONE

                     SIGNAL

------------------------------------------------------------

Represents a directional trading signal.

============================================================
"""

from __future__ import annotations

from enum import StrEnum


class Signal(StrEnum):
    LONG = "LONG"

    SHORT = "SHORT"

    FLAT = "FLAT"
