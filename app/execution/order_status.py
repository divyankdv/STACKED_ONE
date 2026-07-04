"""
============================================================

                    STACKED ONE

                 ORDER STATUS

============================================================
"""

from __future__ import annotations

from enum import Enum


class OrderStatus(str, Enum):

    PENDING = "PENDING"

    SUBMITTED = "SUBMITTED"

    FILLED = "FILLED"

    PARTIALLY_FILLED = "PARTIALLY_FILLED"

    CANCELLED = "CANCELLED"

    REJECTED = "REJECTED"