"""
============================================================

                    STACKED ONE

          BASE COMPOSITE ANALYTICS ENGINE

------------------------------------------------------------

Base class for all composite analytics engines.

Composite engines consume AnalyticsSnapshot instead
of TradeMessage.

Examples

✓ Liquidity Engine
✓ Exhaustion Engine
✓ Smart Money Engine
✓ Regime Engine
✓ Feature Engine

============================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class CompositeAnalyticsEngine(ABC):

    """
    Base class for second-level analytics.
    """

    snapshot_name: str
        #
    # Required snapshots that must exist
    # before this engine can execute.
    #

    dependencies: list[str] = []

    # =====================================================
    # Update
    # =====================================================

    @abstractmethod
    def update(self, analytics_snapshot):

        """
        Consume AnalyticsSnapshot.
        """

        raise NotImplementedError

    # =====================================================
    # Reset
    # =====================================================

    @abstractmethod
    def reset(self):

        raise NotImplementedError

    # =====================================================
    # Snapshot
    # =====================================================

    @abstractmethod
    def snapshot(self):

        raise NotImplementedError