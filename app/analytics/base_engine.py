"""
============================================================

                    STACKED ONE

                BASE ANALYTICS ENGINE

------------------------------------------------------------

Base class for every analytics engine.

Every analytics engine must inherit from this class.

============================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AnalyticsEngine(ABC):

    """
    Base class for all analytics engines.
    """

    # Name used by AnalyticsManager
    snapshot_name: str

    # =====================================================
    # Update Trade
    # =====================================================

    @abstractmethod
    def update_trade(self, trade):

        """
        Process one TradeMessage.
        """

        raise NotImplementedError

    # =====================================================
    # Reset
    # =====================================================

    @abstractmethod
    def reset(self):

        """
        Reset internal state.
        """

        raise NotImplementedError

    # =====================================================
    # Snapshot
    # =====================================================

    @abstractmethod
    def snapshot(self):

        """
        Return immutable snapshot.
        """

        raise NotImplementedError