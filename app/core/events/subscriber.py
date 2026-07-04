"""
============================================================

                    STACKED ONE

                  EVENT SUBSCRIBER

------------------------------------------------------------

Base class for every Event Bus subscriber.

============================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.core.events.event import Event


class Subscriber(ABC):
    """
    Base class for every event subscriber.
    """

    # =====================================================
    # Event Handler
    # =====================================================

    @abstractmethod
    def on_event(

        self,

        event: Event,

    ) -> None:
        """
        Called whenever an event is published.
        """
        raise NotImplementedError

    # =====================================================
    # Optional Name
    # =====================================================

    @property
    def name(self) -> str:

        return self.__class__.__name__

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return self.name

    __repr__ = __str__