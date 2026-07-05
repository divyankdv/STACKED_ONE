"""
============================================================

                    STACKED ONE

                  REPLAY SINK

------------------------------------------------------------

Destination for replayed market data.

ReplayEngine knows only about ReplaySink.

============================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.tick import Tick


class ReplaySink(ABC):
    """
    Destination for replayed Tick objects.
    """

    # =====================================================
    # Consume Tick
    # =====================================================

    @abstractmethod
    def consume(
        self,
        tick: Tick,
    ) -> None:
        """
        Consume one replayed tick.
        """

        raise NotImplementedError
