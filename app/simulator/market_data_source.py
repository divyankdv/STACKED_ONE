"""
============================================================

                    STACKED ONE

                MARKET DATA SOURCE

------------------------------------------------------------

Abstract interface for all market data providers.

Supported implementations:

    • ReplayEngine
    • LiveDataSource
    • CSVDataSource
    • SyntheticDataSource

============================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Iterator

from app.simulator.market_event import MarketEvent


class MarketDataSource(ABC):
    """
    Base interface for all market data sources.
    """

    # =====================================================
    # Iterator
    # =====================================================

    @abstractmethod
    def __iter__(self) -> Iterator[MarketEvent]:
        """
        Returns an iterator over MarketEvent objects.
        """
        raise NotImplementedError

    # =====================================================
    # Reset
    # =====================================================

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the data source back to its initial state.
        """
        raise NotImplementedError

    # =====================================================
    # Finished
    # =====================================================

    @property
    @abstractmethod
    def finished(self) -> bool:
        """
        Returns True when all market events have been consumed.
        """
        raise NotImplementedError

    # =====================================================
    # Event Count
    # =====================================================

    @property
    @abstractmethod
    def event_count(self) -> int:
        """
        Total number of events available.
        """
        raise NotImplementedError

    # =====================================================
    # Current Position
    # =====================================================

    @property
    @abstractmethod
    def current_index(self) -> int:
        """
        Current event index.
        """
        raise NotImplementedError

    # =====================================================
    # Progress
    # =====================================================

    @property
    def progress(self) -> float:
        """
        Returns progress from 0.0 to 1.0.
        """

        if self.event_count == 0:
            return 0.0

        return self.current_index / self.event_count

    # =====================================================
    # Remaining
    # =====================================================

    @property
    def remaining_events(self) -> int:
        """
        Number of remaining events.
        """

        return max(
            self.event_count - self.current_index,
            0,
        )

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (
            f"{self.__class__.__name__}("
            f"{self.current_index}/{self.event_count}"
            ")"
        )

    __repr__ = __str__