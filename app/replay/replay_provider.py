"""
============================================================

                    STACKED ONE

                REPLAY PROVIDER

------------------------------------------------------------

Abstract base class for replay data providers.

============================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import datetime

from app.models.tick import Tick


class ReplayProvider(ABC):
    """
    Base class for every replay provider.
    """

    # =====================================================
    # Load
    # =====================================================

    @abstractmethod
    def load(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
    ) -> None:
        """
        Load replay data into memory.
        """

        raise NotImplementedError

    # =====================================================
    # Iterator
    # =====================================================

    @abstractmethod
    def __iter__(
        self,
    ) -> Iterator[Tick]:

        raise NotImplementedError

    # =====================================================
    # Length
    # =====================================================

    @abstractmethod
    def __len__(
        self,
    ) -> int:

        raise NotImplementedError

    # =====================================================
    # Reset
    # =====================================================

    @abstractmethod
    def reset(
        self,
    ) -> None:

        raise NotImplementedError
