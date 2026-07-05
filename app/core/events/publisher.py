"""
============================================================

                    STACKED ONE

                  EVENT PUBLISHER

------------------------------------------------------------

Base class for objects capable of publishing events.

============================================================
"""

from __future__ import annotations

from app.core.events.event import Event


class Publisher:
    """
    Base publisher used by engines and managers.
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(

        self,

        event_bus=None,

    ):

        self._event_bus = event_bus

    # =====================================================
    # Event Bus
    # =====================================================

    @property
    def event_bus(self):

        return self._event_bus

    def set_event_bus(

        self,

        event_bus,

    ) -> None:

        self._event_bus = event_bus

    # =====================================================
    # Publish
    # =====================================================

    def publish(

        self,

        event: Event,

    ) -> None:

        if self._event_bus is None:

            return

        self._event_bus.publish(

            event,

        )