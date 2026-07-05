"""
============================================================

                    STACKED ONE

                    EVENT

------------------------------------------------------------

Base event object for the STACKED ONE Event Bus.

Every event carries metadata that allows tracing
through the entire trading pipeline.

============================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from app.core.events.event_types import EventType


@dataclass(slots=True, frozen=True)
class Event:
    """
    Immutable event.

    Every event published through the Event Bus is wrapped
    inside this object.
    """

    # =====================================================
    # Identity
    # =====================================================

    event_id: str = field(

        default_factory=lambda: str(uuid4())

    )

    correlation_id: str = field(

        default_factory=lambda: str(uuid4())

    )

    # =====================================================
    # Event Metadata
    # =====================================================

    event_type: EventType = EventType.INFO

    source: str = "Unknown"

    timestamp: datetime = field(

        default_factory=datetime.utcnow

    )

    # =====================================================
    # Market Context
    # =====================================================

    symbol: str = ""

    timeframe: str = ""

    # =====================================================
    # Payload
    # =====================================================

    payload: object | None = None

    # =====================================================
    # Convenience
    # =====================================================

    @property
    def has_payload(self) -> bool:

        return self.payload is not None

    # =====================================================
    # String
    # =====================================================

    def __str__(self):

        return (

            "Event("

            f"type={self.event_type.value}, "

            f"source={self.source}, "

            f"symbol={self.symbol}, "

            f"id={self.event_id[:8]}"

            ")"

        )

    __repr__ = __str__